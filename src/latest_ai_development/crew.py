from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class ResearchPoint(BaseModel):
    topic: str = Field(description="The main topic or area being discussed")
    findings: str = Field(description="The key findings or insights about this topic")
    relevance: str = Field(description="Why this finding is relevant or important")
    sources: List[Dict[str, str]] = Field(
        description="Sources with title and URL for each finding",
        default_factory=list
    )

class ResearchOutput(BaseModel):
    research_points: List[ResearchPoint] = Field(description="List of research findings")
    summary: str = Field(description="Brief summary of overall findings")

class ExecutiveReportSection(BaseModel):
    section_emoji: str = Field(description="Section emoji (e.g., 🔍, 📊, 🎯)")
    section_title: str = Field(description="Section title")
    section_content: str = Field(description="Main content of the section")
    key_insights: List[str] = Field(description="Key insights from this section")
    recommendations: List[str] = Field(
        default_factory=list,
        description="Optional recommendations based on findings"
    )
    sources: List[Dict[str, str]] = Field(
        description="Sources with title and URL for this section",
        default_factory=list
    )

class ExecutiveReport(BaseModel):
    report_title: str = Field(description="Title of the report")
    generation_date: str = Field(description="Report generation date")
    executive_summary: str = Field(description="A concise executive summary")
    key_findings: List[Dict[str, str]] = Field(
        description="List of key findings with their sources",
        default_factory=list
    )
    report_sections: List[ExecutiveReportSection] = Field(
        description="Detailed report sections"
    )
    next_steps: List[str] = Field(description="Recommended next steps")
    sources: List[Dict[str, str]] = Field(
        description="All sources used in the report",
        default_factory=list
    )
	
@CrewBase
class LatestAiDevelopmentCrew():
    """LatestAiDevelopment crew"""

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )
    @agent
    def formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['formatter'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            output_json=ResearchOutput
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_pydantic=ExecutiveReport
        )

    @task
    def formatting_task(self) -> Task:
        return Task(
            config=self.tasks_config['formatting_task']
        )
		
    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
