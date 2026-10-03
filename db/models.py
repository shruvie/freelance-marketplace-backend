from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base

# Association tables
freelancer_skills = Table(
    'freelancer_skills',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

project_skills = Table(
    'project_skills',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) # client, freelancer, admin
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    profile = relationship("Profile", back_populates="user", uselist=False)
    skills = relationship("Skill", secondary=freelancer_skills, back_populates="freelancers")
    
    projects_as_client = relationship("Project", back_populates="client")
    proposals_as_freelancer = relationship("Proposal", back_populates="freelancer")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    profile_image = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    hourly_rate = Column(Float, nullable=True)
    experience_years = Column(Integer, nullable=True)
    
    user = relationship("User", back_populates="profile")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    freelancers = relationship("User", secondary=freelancer_skills, back_populates="skills")
    projects = relationship("Project", secondary=project_skills, back_populates="required_skills")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="open") # open, in_progress, completed, cancelled
    attachments = Column(Text, nullable=True) # JSON string of URLs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    client = relationship("User", back_populates="projects_as_client")
    required_skills = relationship("Skill", secondary=project_skills, back_populates="projects")
    proposals = relationship("Proposal", back_populates="project")
    contracts = relationship("Contract", back_populates="project")

class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    freelancer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    cover_letter = Column(Text, nullable=False)
    proposed_price = Column(Float, nullable=False)
    estimated_delivery = Column(String, nullable=False)
    status = Column(String, default="pending") # pending, accepted, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    freelancer = relationship("User", back_populates="proposals_as_freelancer")
    project = relationship("Project", back_populates="proposals")
    contract = relationship("Contract", back_populates="proposal", uselist=False)

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    freelancer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=False)
    status = Column(String, default="active") # active, completed, cancelled
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    expected_completion_date = Column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="contracts")
    proposal = relationship("Proposal", back_populates="contract")
    milestones = relationship("Milestone", back_populates="contract")
    payments = relationship("Payment", back_populates="contract")

class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="pending") # pending, submitted, approved, paid
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)

    contract = relationship("Contract", back_populates="milestones")
    payments = relationship("Payment", back_populates="milestone")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    milestone_id = Column(Integer, ForeignKey("milestones.id"), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    provider = Column(String, nullable=True)
    provider_tx_id = Column(String, nullable=True)
    status = Column(String, default="pending") # pending, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    contract = relationship("Contract", back_populates="payments")
    milestone = relationship("Milestone", back_populates="payments")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=True)
    message = Column(Text, nullable=False)
    attachments = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AiConversation(Base):
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    messages = relationship("AiMessage", back_populates="conversation")

class AiMessage(Base):
    __tablename__ = "ai_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("ai_conversations.id"), nullable=False)
    role = Column(String, nullable=False) # user, assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("AiConversation", back_populates="messages")
