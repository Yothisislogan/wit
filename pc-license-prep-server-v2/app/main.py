from __future__ import annotations

import random
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload
from starlette.middleware.sessions import SessionMiddleware

from .auth import configured_providers, dev_login, login_redirect, oauth_callback, public_user, require_user
from .content_loader import seed_course_if_empty
from .database import SessionLocal, create_all, get_db
from .models import AnswerChoice, Lesson, LessonProgress, MistakeBank, Module, Question, QuizAnswer, QuizAttempt, Term, User
from .settings import settings
from .tutor import ask_coverage_coach

FRONTEND_DIR = __import__("pathlib").Path(__file__).resolve().parent.parent / "frontend"


class LessonProgressIn(BaseModel):
    completed: bool = True
    confidence: int = Field(default=0, ge=0, le=3)
    notes: str = Field(default="", max_length=5000)
    saved_for_review: bool = False


class QuizSubmitIn(BaseModel):
    mode: str = Field(default="practice", max_length=50)
    answers: dict[int, int] = Field(default_factory=dict, description="question_id -> selected_choice_id")


class TutorAskIn(BaseModel):
    message: str = Field(min_length=2, max_length=1200)


class CourseIn(BaseModel):
    course: str = Field(pattern="^(pc|lh)$")


class StateIn(BaseModel):
    state: str = Field(min_length=2, max_length=2, pattern="^[A-Z]{2}$")


STATE_EXAM_INFO: dict[str, Any] = {
  "AL": {"state_name":"Alabama","vendor":"University of Alabama (self-administered)","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Commissioner powers and duties","Licensing and appointments","Unfair trade practices","Alabama Insurance Guaranty Association","Replacement rules","Marketing practices"],"outline_url":"https://aldoi.gov"},
  "AK": {"state_name":"Alaska","vendor":"Pearson VUE","pc_exam":{"general":100,"state":40,"total_scored":140,"passing_score":70},"lh_exam":{"general":100,"state":40,"total_scored":140,"passing_score":70},"state_topics":["Director of Insurance powers","Definitions and insurer types","Licensing and appointments","Marketing practices and unfair trade practices","Alaska Insurance Guaranty Association","Life-specific: policy provisions, replacement, group life"],"outline_url":"https://www.pearsonvue.com/us/en/ak/insurance.html"},
  "AZ": {"state_name":"Arizona","vendor":"Prometric","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Licensing requirements and disciplinary actions","State regulation of insurance transactions","Unfair practices (misrepresentation, rebating, discrimination, fraud)","Federal laws (ACA, Mental Health Parity, GINA, FCRA, GLBA)"],"outline_url":"https://www.prometric.com/arizona-insurance"},
  "AR": {"state_name":"Arkansas","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":50,"state":30,"total_scored":80,"passing_score":70},"state_topics":["Commissioner powers","Licensing and appointments","Unfair trade practices","Arkansas Life and Health Guaranty Association","Replacement rules","State-mandated health benefits"],"outline_url":"https://www.pearsonvue.com/us/en/ar/insurance.html"},
  "CA": {"state_name":"California","vendor":"PSI","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Insurance Commissioner authority (elected, not appointed)","Unfair Practices Act (only Commissioner may prosecute)","Privacy: GLBA and California Insurance Information and Privacy Protection Act","California Life and Health Insurance Guarantee Association","False/fraudulent claims and unfair discrimination","Licensing: filing, renewal, continuing education, fiduciary duties"],"outline_url":"https://www.psiexams.com"},
  "CO": {"state_name":"Colorado","vendor":"Pearson VUE","pc_exam":{"general":100,"state":20,"total_scored":120,"passing_score":70},"lh_exam":{"general":100,"state":20,"total_scored":120,"passing_score":70},"state_topics":["Commissioner powers, hearings, penalties","Producer licensing and responsibilities","Unfair competition and deceptive practices","Replacement and advertising rules","Annuity suitability standards"],"outline_url":"https://www.pearsonvue.com/us/en/co/insurance.html"},
  "CT": {"state_name":"Connecticut","vendor":"Pearson VUE","pc_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"lh_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"state_topics":["Commissioner duties and powers","Licensing types and maintenance","Agent responsibilities and fiduciary duties","Marketing practices and privacy (IIPPA, FCRA)","Life-specific: solicitation, replacement, standard provisions, annuities"],"outline_url":"https://www.pearsonvue.com/us/en/ct/insurance.html"},
  "DE": {"state_name":"Delaware","vendor":"Pearson VUE","pc_exam":{"general":100,"state":40,"total_scored":140,"passing_score":70},"lh_exam":{"general":100,"state":40,"total_scored":140,"passing_score":70},"state_topics":["Licensing and appointments","Marketing practices and ethics (rebating, twisting, fraud)","Insurance Commissioner powers","Guaranty association and policy statutes","Ethics: types of authority (express, implied, apparent), suitability, advertising"],"outline_url":"https://www.pearsonvue.com/us/en/de/insurance.html"},
  "DC": {"state_name":"District of Columbia","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Commissioner powers and definitions","Licensing requirements and appointments","Unfair trade practices (rebating, misrepresentation, twisting, churning)","Fiduciary duties and AIDS/HIV law","DC Life and Health Insurance Guaranty Association"],"outline_url":"https://www.pearsonvue.com/us/en/dc/insurance.html"},
  "FL": {"state_name":"Florida","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Regulatory structure: CFO, Financial Services Commission, DFS and OIR","Definitions and licensing (agent vs. agency, appointments)","Agent fiduciary duties and premium handling","Guaranty fund and ethics requirement","Unfair practices: sliding, coercion, misrepresentation, twisting, churning, rebating","Replacement and suitability/best-interest rules"],"outline_url":"https://www.pearsonvue.com/us/en/fl/insurance.html"},
  "GA": {"state_name":"Georgia","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Commissioner of Insurance powers","Insurance definitions (domestic, foreign, alien, authorized)","Licensing of agents and counselors","Unfair trade practices and fiduciary duties","Georgia Life and Health Insurance Guaranty Association","Replacement regulations (Reg 120-2-24)"],"outline_url":"https://www.pearsonvue.com/us/en/ga/insurance.html"},
  "HI": {"state_name":"Hawaii","vendor":"Pearson VUE","pc_exam":{"general":100,"state":35,"total_scored":135,"passing_score":70},"lh_exam":{"general":100,"state":35,"total_scored":135,"passing_score":70},"state_topics":["Insurance Commissioner authority","Definitions and types of insurers","Licensing and maintenance","Marketing practices and premium handling","Hawaii Insurance Guaranty Association","Life-specific: replacement, annuity suitability, variable contracts, spousal rights"],"outline_url":"https://www.pearsonvue.com/us/en/hi/insurance.html"},
  "ID": {"state_name":"Idaho","vendor":"Pearson VUE","pc_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"lh_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"state_topics":["Director of Insurance responsibilities","Insurance definitions (admitted, non-admitted, domestic, foreign, alien)","Licensing and appointments","Producer responsibilities and contracts","Unfair trade practices (rebating, misrepresentation, twisting, fraud)"],"outline_url":"https://www.pearsonvue.com/us/en/id/insurance.html"},
  "IL": {"state_name":"Illinois","vendor":"Pearson VUE","pc_exam":{"general":100,"state":33,"total_scored":133,"passing_score":70},"lh_exam":{"general":50,"state":31,"total_scored":81,"passing_score":70},"state_topics":["Director of Insurance powers and examinations","Producer licensing and registration","Fiduciary duties and compensation","Unfair marketing practices (misrepresentation, rebating, twisting, churning)","Life regulations: advertising (Reg 2001/2008), replacement (Reg 917), illustrations","Illinois Life and Health Insurance Guaranty Association"],"outline_url":"https://www.pearsonvue.com/us/en/il/insurance.html"},
  "IN": {"state_name":"Indiana","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Commissioner appointment and powers","Indiana Life and Health Insurance Guaranty Association","Producer licensing types and maintenance","Producer/company compliance and unfair practices (twisting, rebating, misrepresentation)"],"outline_url":"https://www.pearsonvue.com/us/en/in/insurance.html"},
  "IA": {"state_name":"Iowa","vendor":"Pearson VUE","pc_exam":{"general":100,"state":27,"total_scored":127,"passing_score":70},"lh_exam":{"general":100,"state":27,"total_scored":127,"passing_score":70},"state_topics":["Commissioner of Insurance powers","Licensing and appointments","Unfair and deceptive practices (Iowa Insurance Fraud Act)","Iowa Life and Health Insurance Guaranty Association","Life-specific: replacement, group life, viatical settlements, suitability"],"outline_url":"https://www.pearsonvue.com/us/en/ia/insurance.html"},
  "KS": {"state_name":"Kansas","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Commissioner of Insurance (elected)","Licensing and appointments","Unfair/deceptive practices (rebating, misrepresentation, twisting)","Kansas Life and Health Insurance Guaranty Association","Life-specific: replacement, standard provisions, annuity suitability, viatical settlements"],"outline_url":"https://www.pearsonvue.com/us/en/ks/insurance.html"},
  "KY": {"state_name":"Kentucky","vendor":"Kentucky DOI (self-administered)","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Kentucky Insurance Code scope and definitions","Agent licensing requirements (KRS 304.9-080 to 120)","Change of address and license renewal","Record retention requirements","Kentucky Insurance Guaranty Association"],"outline_url":"https://insurance.ky.gov"},
  "LA": {"state_name":"Louisiana","vendor":"PSI","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":50,"state":30,"total_scored":80,"passing_score":70},"state_topics":["Licensing types and maintenance","Disciplinary actions and penalties","Commissioner duties and company regulation","Marketing practices: controlled business, advertising, replacement, illustrations","Unfair trade practices (misrepresentation, rebating, defamation, discrimination)","Insurance Fraud Act and privacy"],"outline_url":"https://www.psiexams.com"},
  "ME": {"state_name":"Maine","vendor":"Pearson VUE","pc_exam":{"general":100,"state":20,"total_scored":120,"passing_score":70},"lh_exam":{"general":50,"state":20,"total_scored":70,"passing_score":70},"state_topics":["Superintendent of Insurance powers","Definitions and Guaranty Association","Licensing types and limitations","Marketing practices (unfair claims, rebating, twisting, misrepresentation)","Producer responsibilities and privacy","Life-specific: solicitation, AIDS rules, standard provisions, viatical settlements, replacement"],"outline_url":"https://www.pearsonvue.com/us/en/me/insurance.html"},
  "MD": {"state_name":"Maryland","vendor":"Prometric","pc_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"lh_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"state_topics":["License renewal and continuing education (24 hrs per cycle including 3 hrs ethics)","Commissioner authority and definitions","Licensing and appointments","Market conduct and consumer protection (rebating, misrepresentation, twisting)","Maryland Life and Health Insurance Guaranty Association"],"outline_url":"https://www.prometric.com/exams/mia/"},
  "MA": {"state_name":"Massachusetts","vendor":"Prometric (transitioning to Pearson VUE July 22 2026)","pc_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"lh_exam":{"general":50,"state":25,"total_scored":75,"passing_score":70},"state_topics":["Licensing process and types of licensees","Disciplinary actions","Commissioner duties and company regulation","Unfair Insurance Practices Act (misrepresentation, false advertising, defamation, rebating)","Insurance Fraud and Privacy Protection Act"],"outline_url":"https://www.prometric.com/exams/insurance-ma/"},
  "MI": {"state_name":"Michigan","vendor":"PSI","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":50,"state":30,"total_scored":80,"passing_score":70},"state_topics":["Company regulation and producer appointments","Types of licensees and license maintenance","Unfair insurance trade practices","Life-specific: advertising, Michigan Life and Health Insurance Guaranty Association, replacement, illustrations"],"outline_url":"https://www.psiexams.com"},
  "MN": {"state_name":"Minnesota","vendor":"Pearson VUE","pc_exam":{"general":100,"state":20,"total_scored":120,"passing_score":70},"lh_exam":{"general":100,"state":20,"total_scored":120,"passing_score":70},"state_topics":["Commissioner powers and definitions","Licensing and appointments","Trade practices and marketing standards (rebating, twisting, churning, misrepresentation)","P&C specific: Standard Fire Policy, FAIR Plan, no-fault auto, Minnesota Auto Insurance Plan, workers compensation"],"outline_url":"https://www.pearsonvue.com/us/en/mn/insurance.html"},
  "MS": {"state_name":"Mississippi","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Commissioner powers and definitions","Licensing and appointments","Market conduct and unfair practices (rebating, twisting, misrepresentation, fraud)","Mississippi Life and Health Insurance Guaranty Association","Replacement and disclosure"],"outline_url":"https://www.pearsonvue.com/us/en/ms/insurance.html"},
  "MO": {"state_name":"Missouri","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Director of Commerce and Insurance powers","Licensing requirements and maintenance","Unfair/deceptive practices (rebating, misrepresentation, defamation)","Missouri Property and Casualty and Life and Health Guaranty Associations","Life-specific: replacement, variable products, group insurance, suitability/best-interest standard"],"outline_url":"https://www.pearsonvue.com/us/en/mo/insurance.html"},
  "MT": {"state_name":"Montana","vendor":"Pearson VUE","pc_exam":{"general":100,"state":24,"total_scored":124,"passing_score":70},"lh_exam":{"general":100,"state":24,"total_scored":124,"passing_score":70},"state_topics":["Commissioner powers and definitions","Licensing requirements","Unfair trade practices (false advertising, rebating, twisting, misrepresentation)","Licensee responsibilities and privacy (Life and Health Guaranty Association, Insurance Fraud Protection Act)","Life-specific: replacement, group life, annuity suitability, viatical settlements, credit life, variable products"],"outline_url":"https://www.pearsonvue.com/us/en/mt/insurance.html"},
  "NE": {"state_name":"Nebraska","vendor":"PSI","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Licensing issuance and maintenance","Types of licenses and exemptions","State regulation of producers and insurers (fiduciary duties, commissions, recordkeeping)","Unfair trade practices (rebating, twisting, misrepresentation, STOLI/IOLI, commingling)","Insurance Fraud Act and privacy (FCRA, CAN-SPAM)"],"outline_url":"https://www.psiexams.com"},
  "NV": {"state_name":"Nevada","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Commissioner and definitions","Licensing and appointments (including prepaid funeral contract agents, reinsurance intermediaries)","Marketing practices and fiduciary duties","Nevada Life and Health Insurance Guaranty Association","Life-specific: credit life, group life, advertising, replacement, viatical settlements"],"outline_url":"https://www.pearsonvue.com/us/en/nv/insurance.html"},
  "NH": {"state_name":"New Hampshire","vendor":"PSI","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":50,"state":30,"total_scored":80,"passing_score":70},"state_topics":["Licensing process and types","State regulation and Commissioner powers","Producer obligations and unfair practices (misrepresentation, rebating, discrimination, fraud)","Auto-insurance statutes (collision deductible waivers, cancellation/non-renewal)","NFIP flood insurance","Federal laws (FCRA, 18 USC 1033/1034)"],"outline_url":"https://www.psiexams.com"},
  "NJ": {"state_name":"New Jersey","vendor":"PSI","pc_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"lh_exam":{"general":50,"state":25,"total_scored":75,"passing_score":70},"state_topics":["Regulatory jurisdiction and Commissioner powers (Paul v. Virginia, McCarran-Ferguson)","Definitions and types of insurers","Licensing and contractual relationships","Trade practices and licensee responsibilities (Fraud Prevention Act, privacy)","New Jersey Life and Health Insurance Guaranty Association","Life-specific: credit life, group life, replacement, suitability"],"outline_url":"https://www.psiexams.com"},
  "NM": {"state_name":"New Mexico","vendor":"Prometric","pc_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"lh_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"state_topics":["Licensing process and types","State regulation and Superintendent powers","Unfair trade practices (misrepresentation, twisting, defamation, rebating, fraud)","Federal regulation (FCRA, federal fraud statute)","Consumer Information Privacy Act"],"outline_url":"https://www.prometric.com/newmexico-insurance"},
  "NY": {"state_name":"New York","vendor":"PSI","pc_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"lh_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"state_topics":["Agent appointments and termination","Unfair and prohibited practices (misrepresentation, defamation, rebating)","Licensee regulation (controlled business, commissions, trust accounts, compensation disclosure)","Examination of books and records","Fraud and privacy (Insurance Frauds Prevention Act, FCRA, 18 USC 1033)","NY-specific: Valued Policy Law, Regulation 60 (replacement), Regulation 187 (best interest), NY FAIR Plan, no-fault auto"],"outline_url":"https://www.psiexams.com"},
  "NC": {"state_name":"North Carolina","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Contract of insurance and definitions","Commissioner of Insurance powers","Licensing of intermediaries and continuing education","Privacy: Insurance Information and Privacy Protection Act","Unfair Trade Practices Act (Article 63)","Solicitation rules, replacement regulations, ethical standards","NC Life and Health Insurance Guaranty Association"],"outline_url":"https://www.pearsonvue.com/us/en/nc/insurance.html"},
  "ND": {"state_name":"North Dakota","vendor":"PSI","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":50,"state":30,"total_scored":80,"passing_score":70},"state_topics":["Licensing and appointments","State regulation and producer obligations","Unfair trade practices and insurance fraud","A&H policy provisions and mandated benefits (newborns, dependents, portability, prescriptions, chiropractic)","North Dakota Life and Health Guaranty Association"],"outline_url":"https://www.psiexams.com"},
  "OH": {"state_name":"Ohio","vendor":"PSI","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Director of Insurance powers and company regulation","Agent licensing and appointments","Unfair trade practices and market conduct","Ohio-specific: Valued Policy Law, Ohio Insurance Guaranty Association, mine-subsidence coverage, workers compensation monopoly","Federal laws (FCRA, 18 USC 1033)"],"outline_url":"https://www.psiexams.com"},
  "OK": {"state_name":"Oklahoma","vendor":"PSI","pc_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"lh_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"state_topics":["Commissioner powers and definitions","Licensing and compensation rules","P&C adjuster topics: Oklahoma Insurance Guaranty Association, cancellation/non-renewal, surplus lines, unfair claims settlement"],"outline_url":"https://www.psiexams.com"},
  "OR": {"state_name":"Oregon","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Licensing requirements and maintenance","Regulator powers and appointments","Market conduct and unfair practices (rebating, misrepresentation, defamation, fraud)","Oregon Insurance Guaranty Association, Oregon FAIR Plan","Insurance Fraud Prevention Act and privacy"],"outline_url":"https://www.pearsonvue.com/us/en/or/insurance.html"},
  "PA": {"state_name":"Pennsylvania","vendor":"PSI","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":50,"state":30,"total_scored":80,"passing_score":70},"state_topics":["Licensing process and types","Regulatory authority and company regulation","Producer regulation and market conduct (rebating, twisting, misrepresentation, fraud)","Privacy and fraud (FCRA, GLBA, Insurance Fraud Regulation)","PA-specific: MVFRL (Motor Vehicle Financial Responsibility Law)"],"outline_url":"https://www.psiexams.com"},
  "RI": {"state_name":"Rhode Island","vendor":"Pearson VUE","pc_exam":{"general":100,"state":40,"total_scored":140,"passing_score":70},"lh_exam":{"general":100,"state":40,"total_scored":140,"passing_score":70},"state_topics":["Commissioner authority and definitions","Licensing and appointments","Market conduct and unfair practices (rebating, twisting, misrepresentation, fraud)","Rhode Island Life and Health Insurance Guaranty Association","Life-specific: replacement, AIDS/HIV testing, suitability, group life provisions"],"outline_url":"https://www.pearsonvue.com/us/en/ri/insurance.html"},
  "SC": {"state_name":"South Carolina","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Director powers and definitions","Licensing and appointments","Unfair trade practices (rebating, twisting, misrepresentation, fraud, churning)","South Carolina Life and Accident and Health Insurance Guaranty Association","Life-specific: replacement, advertising, group life provisions"],"outline_url":"https://www.pearsonvue.com/us/en/sc/insurance.html"},
  "SD": {"state_name":"South Dakota","vendor":"Pearson VUE","pc_exam":{"general":100,"state":35,"total_scored":135,"passing_score":70},"lh_exam":{"general":100,"state":35,"total_scored":135,"passing_score":70},"state_topics":["Director powers and definitions","Licensing requirements and maintenance","Producer responsibilities and market conduct (rebating, twisting, misrepresentation, commingling, misappropriation)","Policy delivery and life-specific provisions (replacement, standard provisions, group life, viatical settlements)"],"outline_url":"https://www.pearsonvue.com/us/en/sd/insurance.html"},
  "TN": {"state_name":"Tennessee","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Commissioner powers and definitions","Licensing and appointments","Unfair trade and claims practices (false advertising, rebating, misrepresentation, fraud)","Tennessee Life and Health Insurance Guaranty Association","Life-specific: policy provisions, disclosures, replacement, annuity suitability"],"outline_url":"https://www.pearsonvue.com/us/en/tn/insurance.html"},
  "TX": {"state_name":"Texas","vendor":"Pearson VUE","pc_exam":{"general":100,"state":35,"total_scored":135,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"life_only_exam":{"general":50,"state":30,"total_scored":80,"passing_score":70},"state_topics":["Commissioner powers (examinations, investigations, hearings, penalties, cease-and-desist)","Definitions (transacting insurance, domestic/foreign/alien, stock/mutual/fraternal)","Licensing (agent/agency, temporary, exemptions, appointments, CE, records, denial/renewal/suspension)","Marketing practices (unfair claims, false advertising, misrepresentation, defamation, rebating, fraud, commingling)","Texas Life and Health Guaranty Association","TX-specific: Texas Windstorm Insurance Association (TWIA)","TX-specific: Transportation network company coverage"],"outline_url":"https://www.pearsonvue.com/content/dam/VUE/vue/en/documents/publications/124401.pdf"},
  "UT": {"state_name":"Utah","vendor":"Prometric","pc_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"lh_exam":{"general":100,"state":25,"total_scored":125,"passing_score":70},"state_topics":["Commissioner powers and licensing","Adjuster licensing qualifications and exemptions","Disciplinary actions and unfair claims laws","Federal fraud statutes (18 USC 1033-1034)"],"outline_url":"https://www.prometric.com/utah-insurance"},
  "VT": {"state_name":"Vermont","vendor":"Prometric","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Licensing process and maintenance","State regulation and Commissioner powers","Unfair trade practices (misrepresentation, rebating, defamation, discrimination, suitability)","Federal laws (FCRA, 18 USC 1033)","Vermont FAIR Plan","Vermont Life and Health Insurance Guaranty Association"],"outline_url":"https://www.prometric.com/exams/insurance-vt/"},
  "VA": {"state_name":"Virginia","vendor":"Prometric","pc_exam":{"general":100,"state":35,"total_scored":135,"passing_score":70},"lh_exam":{"general":100,"state":35,"total_scored":135,"passing_score":70},"state_topics":["Licensing and maintenance (agents, consultants, non-residents, business entities, viatical settlement brokers)","Disciplinary actions and Commission powers","Agent responsibilities and unfair practices (misrepresentation, rebating, twisting, improper referrals)","Privacy and information practices","Virginia Life Accident and Sickness Insurance Guaranty Association"],"outline_url":"https://www.prometric.com/exams/insurance-va/"},
  "WA": {"state_name":"Washington","vendor":"PSI","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Commissioner authority and definitions","Licensing and appointments","Marketing practices (rebating, twisting, misrepresentation, defamation, discrimination)","Disclosure of compensation","Replacement and life-specific rules (illustrations, annuity suitability, policy clauses)","Washington Life and Disability Insurance Guaranty Association"],"outline_url":"https://www.psiexams.com"},
  "WV": {"state_name":"West Virginia","vendor":"Pearson VUE","pc_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"lh_exam":{"general":100,"state":30,"total_scored":130,"passing_score":70},"state_topics":["Commissioner authority","Definitions and licensing types","Unfair trade practices (rebating, misrepresentation, defamation, fraud)","West Virginia Life and Health Insurance Guaranty Association","Replacement, disclosure, and annuity suitability"],"outline_url":"https://www.pearsonvue.com/us/en/wv/insurance.html"},
  "WI": {"state_name":"Wisconsin","vendor":"Prometric","pc_exam":{"general":100,"state":35,"total_scored":135,"passing_score":70},"lh_exam":{"general":50,"state":35,"total_scored":85,"passing_score":70},"state_topics":["Licensing purpose, requirements and maintenance","State regulation and Wisconsin Insurance Security Fund","Producer regulation and marketing practices (rebating, twisting, misrepresentation, defamation)","Company regulation and unfair claims practices","Examination of records and producer-conduct rules"],"outline_url":"https://www.prometric.com/wisconsin-insurance"},
  "WY": {"state_name":"Wyoming","vendor":"Pearson VUE","pc_exam":{"general":100,"state":35,"total_scored":135,"passing_score":70},"lh_exam":{"general":100,"state":35,"total_scored":135,"passing_score":70},"state_topics":["Commissioner appointment and powers","Definitions and licensing types","License maintenance (CE, change of address, renewal, termination)","Producer responsibilities and marketing conduct (rebating, twisting, misrepresentation, fraud)","Wyoming Insurance Guaranty Association and consumer privacy","Wyoming FAIR Plan"],"outline_url":"https://www.pearsonvue.com/us/en/wy/insurance.html"},
}

_STATE_NAMES: dict[str, str] = {k: v["state_name"] for k, v in STATE_EXAM_INFO.items()}


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all()
    db = SessionLocal()
    try:
        for stmt in [
            "ALTER TABLE users ADD COLUMN course VARCHAR(20) DEFAULT 'pc'",
            "ALTER TABLE users ADD COLUMN state VARCHAR(2)",
            "ALTER TABLE modules ADD COLUMN course VARCHAR(20) DEFAULT 'pc'",
            "CREATE TABLE IF NOT EXISTS coach_rate_limits (id INTEGER PRIMARY KEY, user_id INTEGER, window_hour TEXT, window_day TEXT, hour_count INTEGER DEFAULT 0, day_count INTEGER DEFAULT 0)",
            "CREATE INDEX IF NOT EXISTS idx_coach_rate_user ON coach_rate_limits(user_id)",
        ]:
            try:
                db.execute(text(stmt))
                db.commit()
            except Exception:
                db.rollback()
        seed_course_if_empty(db)
    finally:
        db.close()
    yield


app = FastAPI(title="P&C License Prep Academy API", version="2.1.0", lifespan=lifespan)
origins = settings.cors_origin_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False if origins == ["*"] else True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret, same_site="lax", https_only=settings.app_base_url.startswith("https"))

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


def module_out(module: Module) -> dict[str, Any]:
    return {
        "id": module.id,
        "slug": module.slug,
        "title": module.title,
        "description": module.description,
        "sort_order": module.sort_order,
        "lesson_count": len(module.lessons),
    }


def lesson_out(lesson: Lesson) -> dict[str, Any]:
    return {
        "id": lesson.id,
        "slug": lesson.slug,
        "module_id": lesson.module_id,
        "title": lesson.title,
        "summary": lesson.summary,
        "body": lesson.body,
        "example": lesson.example,
        "memory_tip": lesson.memory_tip,
        "audio_script": lesson.audio_script,
        "estimated_minutes": lesson.estimated_minutes,
        "sort_order": lesson.sort_order,
    }


def question_out(question: Question, include_answer: bool = False) -> dict[str, Any]:
    data = {
        "id": question.id,
        "module_id": question.module_id,
        "lesson_id": question.lesson_id,
        "question_text": question.question_text,
        "question_type": question.question_type,
        "difficulty": question.difficulty,
        "choices": [
            {
                "id": c.id,
                "choice_text": c.choice_text,
                "explanation": c.explanation if include_answer else "",
                "sort_order": c.sort_order,
                **({"is_correct": c.is_correct} if include_answer else {}),
            }
            for c in question.choices
        ],
        "explanation": question.explanation if include_answer else "",
    }
    return data


@app.get("/")
def home():
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"ok": True, "app": settings.app_name}


@app.get("/api/health")
def health(db: Session = Depends(get_db)):
    return {
        "ok": True,
        "version": "2.1.0",
        "modules": db.scalar(select(func.count()).select_from(Module)),
        "lessons": db.scalar(select(func.count()).select_from(Lesson)),
        "questions": db.scalar(select(func.count()).select_from(Question)),
        "providers": configured_providers(),
        "free_public_access": True,
        "coverage_coach_mode": settings.coverage_coach_provider if settings.gemini_api_key else ("openai" if settings.openai_api_key else "fallback"),
    }


@app.get("/auth/providers")
def auth_providers():
    return {"providers": configured_providers(), "dev_login_enabled": settings.enable_dev_login}


@app.get("/auth/login/{provider}")
async def login(provider: str, request: Request):
    return await login_redirect(request, provider)


@app.get("/auth/callback/{provider}")
async def callback(provider: str, request: Request, db: Session = Depends(get_db)):
    return await oauth_callback(request, db, provider)


@app.get("/auth/dev-login")
def dev(request: Request, db: Session = Depends(get_db)):
    return dev_login(request, db)


@app.post("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}


@app.get("/api/me")
def me(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return {"user": None}
    user = db.get(User, int(user_id))
    if not user:
        return {"user": None}
    base = public_user(user)
    course = getattr(user, "course", "pc") or "pc"
    state = getattr(user, "state", None)
    state_name = STATE_EXAM_INFO.get(state or "", {}).get("state_name") if state else None
    return {"user": {**base, "course": course, "state": state, "state_name": state_name}}


@app.post("/api/me/course")
def set_course(payload: CourseIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    user.course = payload.course
    db.commit()
    return {"ok": True, "course": user.course}


@app.post("/api/me/state")
def set_state(payload: StateIn, request: Request, db: Session = Depends(get_db)):
    if payload.state not in STATE_EXAM_INFO:
        raise HTTPException(status_code=422, detail=f"Unknown state abbreviation: {payload.state}")
    user = require_user(request, db)
    user.state = payload.state
    db.commit()
    return {"ok": True, "state": user.state, "state_name": _STATE_NAMES[user.state]}


@app.get("/api/state-info/{state_abbr}")
def state_info(state_abbr: str):
    abbr = state_abbr.upper()
    if abbr not in STATE_EXAM_INFO:
        raise HTTPException(status_code=404, detail="State not found")
    info = STATE_EXAM_INFO[abbr]
    return {"state": abbr, **info}


@app.get("/api/modules")
def list_modules(request: Request, course: str | None = Query(None), db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not course and user_id:
        u = db.get(User, int(user_id))
        course = getattr(u, "course", "pc") if u else "pc"
    stmt = select(Module).options(selectinload(Module.lessons)).where(Module.is_active == True)
    if course:
        stmt = stmt.where(Module.course == course)
    stmt = stmt.order_by(Module.sort_order, Module.id)
    modules = db.scalars(stmt).all()
    return [module_out(m) for m in modules]


@app.get("/api/modules/{slug}")
def get_module(slug: str, db: Session = Depends(get_db)):
    module = db.scalar(select(Module).options(selectinload(Module.lessons)).where(Module.slug == slug, Module.is_active == True))
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return {**module_out(module), "lessons": [lesson_out(l) for l in module.lessons if l.is_active]}


@app.get("/api/lessons/{slug}")
def get_lesson(slug: str, db: Session = Depends(get_db)):
    lesson = db.scalar(select(Lesson).where(Lesson.slug == slug, Lesson.is_active == True))
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    terms = db.scalars(select(Term).where(Term.module_id == lesson.module_id).order_by(Term.term)).all()
    module = db.scalar(select(Module).where(Module.id == lesson.module_id))
    return {
        **lesson_out(lesson),
        "module_slug": module.slug if module else "",
        "module_title": module.title if module else "",
        "terms": [term_out(t) for t in terms],
    }


def term_out(term: Term) -> dict[str, Any]:
    return {
        "id": term.id,
        "module_id": term.module_id,
        "lesson_id": term.lesson_id,
        "term": term.term,
        "plain_english_definition": term.plain_english_definition,
        "exam_definition": term.exam_definition,
        "example": term.example,
    }


@app.get("/api/terms")
def list_terms(module_slug: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Term).order_by(Term.term)
    if module_slug:
        stmt = stmt.join(Module).where(Module.slug == module_slug)
    return [term_out(t) for t in db.scalars(stmt).all()]


@app.get("/api/questions")
def list_questions(module_slug: str | None = None, limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    stmt = select(Question).options(selectinload(Question.choices)).where(Question.is_active == True)
    if module_slug:
        stmt = stmt.join(Module).where(Module.slug == module_slug)
    questions = list(db.scalars(stmt).all())
    random.shuffle(questions)
    return [question_out(q) for q in questions[:limit]]


@app.post("/api/quiz/submit")
def submit_quiz(payload: QuizSubmitIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    if len(payload.answers) > 50:
        raise HTTPException(status_code=400, detail="Submit 50 answers or fewer at a time")

    attempt = QuizAttempt(user_id=user.id, mode=payload.mode, total_questions=len(payload.answers))
    db.add(attempt)
    db.flush()

    correct_count = 0
    results = []
    for question_id, choice_id in payload.answers.items():
        question = db.scalar(select(Question).options(selectinload(Question.choices)).where(Question.id == question_id))
        choice = db.get(AnswerChoice, choice_id)
        if not question or not choice or choice.question_id != question.id:
            raise HTTPException(status_code=400, detail="Invalid question or answer choice")
        is_correct = bool(choice.is_correct)
        correct_count += 1 if is_correct else 0
        db.add(QuizAnswer(attempt_id=attempt.id, question_id=question.id, selected_choice_id=choice.id, is_correct=is_correct))
        if not is_correct:
            mistake = db.scalar(select(MistakeBank).where(MistakeBank.user_id == user.id, MistakeBank.question_id == question.id))
            if mistake:
                mistake.times_missed += 1
                mistake.mastered_at = None
            else:
                db.add(MistakeBank(user_id=user.id, question_id=question.id, times_missed=1))
        results.append({"question": question_out(question, include_answer=True), "selected_choice_id": choice.id, "is_correct": is_correct})

    attempt.score = round(correct_count / max(len(payload.answers), 1) * 100)
    db.commit()
    return {"attempt_id": attempt.id, "score": attempt.score, "correct": correct_count, "total": len(payload.answers), "results": results}


@app.get("/api/progress")
def progress(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    total_lessons = db.scalar(select(func.count()).select_from(Lesson).where(Lesson.is_active == True)) or 0
    progress_rows = db.scalars(select(LessonProgress).where(LessonProgress.user_id == user.id)).all()
    completed = sum(1 for p in progress_rows if p.completed)
    mistakes = db.scalar(select(func.count()).select_from(MistakeBank).where(MistakeBank.user_id == user.id)) or 0
    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed,
        "percent_complete": round(completed / max(total_lessons, 1) * 100),
        "mistake_count": mistakes,
        "items": [
            {
                "lesson_id": p.lesson_id,
                "completed": p.completed,
                "confidence": p.confidence,
                "notes": p.notes,
                "saved_for_review": p.saved_for_review,
            }
            for p in progress_rows
        ],
    }


@app.post("/api/lessons/{lesson_id}/progress")
def save_lesson_progress(lesson_id: int, payload: LessonProgressIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    row = db.scalar(select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson.id))
    if not row:
        row = LessonProgress(user_id=user.id, lesson_id=lesson.id)
        db.add(row)
    row.completed = payload.completed
    row.confidence = payload.confidence
    row.notes = payload.notes
    row.saved_for_review = payload.saved_for_review
    db.commit()
    return {"ok": True}


@app.get("/api/mistakes")
def mistake_bank(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    rows = db.scalars(select(MistakeBank).options(selectinload(MistakeBank.question).selectinload(Question.choices)).where(MistakeBank.user_id == user.id).order_by(MistakeBank.times_missed.desc())).all()
    return [
        {
            "id": m.id,
            "times_missed": m.times_missed,
            "question": question_out(m.question, include_answer=True),
        }
        for m in rows
    ]


@app.post("/api/tutor/ask")
def tutor_ask(payload: TutorAskIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    return ask_coverage_coach(db, user, payload.message)


class StudioIn(BaseModel):
    action: str
    module_slug: str

@app.post("/api/studio/generate")
def studio_generate(payload: StudioIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    module = db.scalars(select(Module).where(Module.slug == payload.module_slug)).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    lessons = db.scalars(select(Lesson).where(Lesson.module_id == module.id, Lesson.is_active == True).order_by(Lesson.sort_order)).all()
    terms = db.scalars(select(Term).where(Term.module_id == module.id).order_by(Term.term)).all()
    lesson_dicts = [{"title": l.title, "summary": l.summary or "", "body": l.body[:400] if l.body else "", "example": l.example or ""} for l in lessons]
    term_dicts = [{"term": t.term, "plain_english_definition": t.plain_english_definition or "", "exam_definition": t.exam_definition or "", "example": t.example or ""} for t in terms]
    from .tutor import generate_studio_content
    result = generate_studio_content(payload.action, module.title, term_dicts, lesson_dicts)
    return result


@app.get("/privacy")
def privacy_page():
    from fastapi.responses import HTMLResponse
    html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Privacy Policy — WIT</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:800px;margin:0 auto;padding:2rem;line-height:1.7;color:#333}h1{color:#1a1a1a}h2{color:#444;margin-top:2rem}a{color:#1a73e8}.back{display:inline-block;margin-bottom:2rem;color:#1a73e8;text-decoration:none}</style>
</head><body>
<a href="/" class="back">← Back to WIT</a>
<h1>Privacy Policy</h1>
<p><strong>Last updated: June 2026</strong></p>
<p>We Insure Things ("WIT") is committed to protecting your privacy. This policy explains what information we collect and how we use it.</p>
<h2>Information We Collect</h2>
<p>When you sign in with Google or Microsoft, we receive your name and email address. We store your study progress, quiz results, and lesson completions in our database to personalize your learning experience.</p>
<h2>How We Use Your Information</h2>
<p>We use your information solely to provide the WIT exam prep service — tracking your progress, personalizing study recommendations, and powering the Coverage Coach AI tutor. We do not sell your data. We do not share your data with third parties except as required to operate the service (OAuth providers for authentication).</p>
<h2>Coverage Coach AI</h2>
<p>Coverage Coach uses the Google Gemini API to answer your insurance questions. Your questions are sent to Google's API but are not associated with your personal identity — only the question text is transmitted, not your name or email.</p>
<h2>Data Storage</h2>
<p>Your data is stored on dedicated servers. We do not use third-party analytics or advertising services.</p>
<h2>Your Rights</h2>
<p>You may request deletion of your account and all associated data by emailing us at privacy@weinsurethings.com.</p>
<h2>Contact</h2>
<p>Questions? Email us at privacy@weinsurethings.com</p>
</body></html>"""
    return HTMLResponse(html)


@app.get("/terms")
def terms_page():
    from fastapi.responses import HTMLResponse
    html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Terms of Service — WIT</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:800px;margin:0 auto;padding:2rem;line-height:1.7;color:#333}h1{color:#1a1a1a}h2{color:#444;margin-top:2rem}a{color:#1a73e8}.back{display:inline-block;margin-bottom:2rem;color:#1a73e8;text-decoration:none}</style>
</head><body>
<a href="/" class="back">← Back to WIT</a>
<h1>Terms of Service</h1>
<p><strong>Last updated: June 2026</strong></p>
<p>By using We Insure Things ("WIT") you agree to these terms.</p>
<h2>The Service</h2>
<p>WIT provides free insurance licensing exam preparation materials. The service is provided as-is for educational purposes only. WIT is not an accredited educational institution and does not guarantee exam passage.</p>
<h2>Free Forever</h2>
<p>WIT is and will remain free. We will never charge for access to study materials, practice questions, or the Coverage Coach AI tutor.</p>
<h2>Acceptable Use</h2>
<p>You may use WIT for personal study purposes. You may not scrape, copy, or redistribute our content. You may not attempt to circumvent rate limits or abuse the Coverage Coach AI tutor.</p>
<h2>AI Tutor Disclaimer</h2>
<p>Coverage Coach is an AI assistant for exam prep only. It does not provide legal advice, binding insurance opinions, or claim determinations. Always consult a licensed professional for actual insurance matters.</p>
<h2>Intellectual Property</h2>
<p>Study content, questions, and materials on WIT are owned by We Insure Things. The WIT monster mascot and branding are proprietary.</p>
<h2>Limitation of Liability</h2>
<p>WIT is provided free of charge. To the maximum extent permitted by law, We Insure Things is not liable for any damages arising from use of the service.</p>
<h2>Contact</h2>
<p>Questions? Email us at legal@weinsurethings.com</p>
</body></html>"""
    return HTMLResponse(html)


@app.get("/api/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Aggregated progress data for the dashboard view."""
    user = require_user(request, db)

    course = user.course or "pc"

    # ── Lesson completion ────────────────────────────────────────────
    total_lessons = (
        db.scalar(
            select(func.count()).select_from(Lesson)
            .join(Module, Module.id == Lesson.module_id)
            .where(Lesson.is_active == True, Module.course == course)
        ) or 0
    )
    progress_rows = db.scalars(
        select(LessonProgress).where(LessonProgress.user_id == user.id)
    ).all()
    completed_ids = {p.lesson_id for p in progress_rows if p.completed}

    # ── Module breakdown + recommendations ──────────────────────────
    modules = db.scalars(
        select(Module)
        .where(Module.is_active == True, Module.course == course)
        .options(selectinload(Module.lessons))
        .order_by(Module.sort_order)
    ).all()

    module_stats: list[dict] = []
    recommendations: list[dict] = []
    for m in modules:
        active = [l for l in m.lessons if l.is_active]
        done = sum(1 for l in active if l.id in completed_ids)
        pct = round(done / max(len(active), 1) * 100)
        module_stats.append({
            "slug": m.slug,
            "title": m.title,
            "total_lessons": len(active),
            "completed_lessons": done,
            "pct": pct,
        })
        # First incomplete lesson per module → up-next recommendations
        if len(recommendations) < 4:
            for l in sorted(active, key=lambda x: x.sort_order):
                if l.id not in completed_ids:
                    recommendations.append({
                        "lesson_slug": l.slug,
                        "lesson_title": l.title,
                        "module_slug": m.slug,
                        "module_title": m.title,
                        "estimated_minutes": l.estimated_minutes or 7,
                    })
                    break

    # ── Quiz history ─────────────────────────────────────────────────
    recent_attempts = db.scalars(
        select(QuizAttempt)
        .where(QuizAttempt.user_id == user.id)
        .order_by(QuizAttempt.created_at.desc())
        .limit(10)
    ).all()
    avg_quiz = (
        round(sum(a.score for a in recent_attempts) / len(recent_attempts))
        if recent_attempts else 0
    )

    # ── Mistake bank ─────────────────────────────────────────────────
    mistake_count = (
        db.scalar(
            select(func.count()).select_from(MistakeBank).where(MistakeBank.user_id == user.id)
        ) or 0
    )
    top_mistakes = db.scalars(
        select(MistakeBank)
        .options(selectinload(MistakeBank.question))
        .where(MistakeBank.user_id == user.id)
        .order_by(MistakeBank.times_missed.desc())
        .limit(5)
    ).all()

    # ── Readiness score ──────────────────────────────────────────────
    lesson_pct = round(len(completed_ids) / max(total_lessons, 1) * 100)
    mistake_penalty = min(mistake_count * 2, 20)
    readiness = max(0, min(100, round(lesson_pct * 0.5 + avg_quiz * 0.5 - mistake_penalty)))

    return {
        "user": user.name or user.email or "Candidate",
        "readiness": readiness,
        "lessons": {
            "total": total_lessons,
            "completed": len(completed_ids),
            "pct": lesson_pct,
        },
        "quizzes": {
            "total_taken": len(recent_attempts),
            "avg_score": avg_quiz,
            "recent": [
                {
                    "score": a.score,
                    "total": a.total_questions,
                    "date": a.created_at.isoformat() if a.created_at else None,
                }
                for a in recent_attempts[:8]
            ],
        },
        "mistakes": {
            "count": mistake_count,
            "top": [
                {
                    "question": (
                        m.question.question_text[:110] + "…"
                        if m.question and len(m.question.question_text) > 110
                        else (m.question.question_text if m.question else "")
                    ),
                    "times_missed": m.times_missed,
                }
                for m in top_mistakes
            ],
        },
        "modules": module_stats,
        "recommendations": recommendations,
    }
