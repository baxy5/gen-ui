from typing import Annotated
from fastapi import Depends, HTTPException
from agents.dashboard_agent import (
    AgentState,
    DashboardAgent,
)
from langchain_core.runnables.config import RunnableConfig
from core.store_to_r2 import R2ObjectStorage
from schemas.dashboard_schema import RequestSchema, ResponseSchema


class DashboardService:
    """Service for interacing with Dashboard Agent."""

    def __init__(
        self,
        r2: Annotated[
            R2ObjectStorage,
            Depends(
                lambda: R2ObjectStorage(
                    "https://pub-b348006f0b2142f7a105983d74576412.r2.dev"
                )
            ),
        ],
        agent: Annotated[DashboardAgent, Depends()],
    ) -> None:
        self.agent = agent
        self.r2 = r2
        self.data = {
            "companyProfile": {
                "name": "TechNova Solutions",
                "industry": "Enterprise Software",
                "founded": 2005,
                "headquarters": "San Francisco, CA",
                "mission": "Empowering businesses through innovative software solutions",
                "employees": {
                    "total": 1250,
                    "byDepartment": {
                        "engineering": 450,
                        "sales": 320,
                        "marketing": 180,
                        "customerSupport": 220,
                        "administration": 80,
                    },
                    "remotePercentage": 65,
                },
                "leadership": [
                    {"name": "Sarah Chen", "position": "CEO", "yearsInCompany": 15},
                    {
                        "name": "Michael Rodriguez",
                        "position": "CTO",
                        "yearsInCompany": 12,
                    },
                    {
                        "name": "Alicia Washington",
                        "position": "CFO",
                        "yearsInCompany": 8,
                    },
                ],
            },
            "financialOverview": {
                "currentValuation": "$850M",
                "lastFundingRound": {
                    "series": "D",
                    "amount": "$120M",
                    "date": "2022-06-15",
                    "leadInvestor": "Sequoia Capital",
                },
                "revenueStreams": {
                    "subscriptions": 68,
                    "professionalServices": 22,
                    "partnerships": 10,
                },
                "profitMargin": 28.5,
                "growthRate": {"fiveYear": 34.2, "threeYear": 42.7, "oneYear": 23.1},
            },
            "products": [
                {
                    "name": "NovaSuite Enterprise",
                    "category": "Enterprise Resource Planning",
                    "launchYear": 2008,
                    "annualRevenue": 1850000,
                    "marketShare": 22.5,
                    "customers": 450,
                },
                {
                    "name": "CloudSync Platform",
                    "category": "Cloud Integration",
                    "launchYear": 2012,
                    "annualRevenue": 1250000,
                    "marketShare": 18.3,
                    "customers": 620,
                },
                {
                    "name": "SecureID Pro",
                    "category": "Identity Management",
                    "launchYear": 2016,
                    "annualRevenue": 950000,
                    "marketShare": 14.2,
                    "customers": 780,
                },
                {
                    "name": "DataInsight Analytics",
                    "category": "Business Intelligence",
                    "launchYear": 2019,
                    "annualRevenue": 650000,
                    "marketShare": 8.7,
                    "customers": 410,
                },
            ],
            "customerMetrics": {
                "totalCustomers": 2260,
                "customerSegmentation": {
                    "enterprise": 35,
                    "midMarket": 45,
                    "smallBusiness": 20,
                },
                "acquisitionCost": 4200,
                "retentionRate": 92.5,
                "churnRate": 7.5,
                "nps": 72,
                "averageContractValue": 68000,
                "customerLifetimeValue": 420000,
            },
            "marketPosition": {
                "globalRank": 12,
                "competitors": [
                    {
                        "name": "Enterprise Solutions Inc.",
                        "marketShare": 28.5,
                        "competitivePosition": "Leader",
                    },
                    {
                        "name": "CloudSoft Technologies",
                        "marketShare": 24.2,
                        "competitivePosition": "Leader",
                    },
                    {
                        "name": "TechNova Solutions",
                        "marketShare": 18.3,
                        "competitivePosition": "Challenger",
                    },
                    {
                        "name": "Agile Systems",
                        "marketShare": 12.5,
                        "competitivePosition": "Challenger",
                    },
                    {
                        "name": "NextGen Software",
                        "marketShare": 9.8,
                        "competitivePosition": "Niche Player",
                    },
                ],
                "awards": [
                    "Best Enterprise Software 2023 - Tech Excellence Awards",
                    "Innovation Leader 2022 - Business Software Report",
                    "Top Cloud Solution 2021 - Cloud Computing Magazine",
                ],
            },
            "geographicalPresence": {
                "regions": [
                    {
                        "name": "North America",
                        "revenuePercentage": 45,
                        "offices": ["San Francisco", "New York", "Toronto", "Chicago"],
                    },
                    {
                        "name": "Europe",
                        "revenuePercentage": 30,
                        "offices": ["London", "Berlin", "Paris", "Amsterdam"],
                    },
                    {
                        "name": "Asia Pacific",
                        "revenuePercentage": 20,
                        "offices": ["Singapore", "Tokyo", "Sydney", "Bangalore"],
                    },
                    {
                        "name": "Latin America",
                        "revenuePercentage": 5,
                        "offices": ["Sao Paulo", "Mexico City"],
                    },
                ],
                "expansionPlans": [
                    {
                        "region": "Middle East",
                        "plannedOffices": ["Dubai", "Tel Aviv"],
                        "targetDate": "2024-Q3",
                        "projectedInvestment": 8500000,
                    },
                    {
                        "region": "Africa",
                        "plannedOffices": ["Johannesburg", "Nairobi"],
                        "targetDate": "2025-Q2",
                        "projectedInvestment": 7200000,
                    },
                ],
            },
            "yearlyData": [
                {
                    "year": 2005,
                    "revenue": 1250000,
                    "expenses": 850000,
                    "profit": 400000,
                    "profitMargin": 32.0,
                    "employees": 45,
                    "customers": 12,
                    "marketShare": 1.2,
                    "productCount": 1,
                    "r_and_d_spending": 220000,
                    "marketing_spending": 150000,
                    "customer_acquisition_cost": 12500,
                    "customer_retention_rate": 85.0,
                },
                {
                    "year": 2006,
                    "revenue": 1450000,
                    "expenses": 920000,
                    "profit": 530000,
                    "profitMargin": 36.5,
                    "employees": 52,
                    "customers": 18,
                    "marketShare": 1.8,
                    "productCount": 1,
                    "r_and_d_spending": 250000,
                    "marketing_spending": 180000,
                    "customer_acquisition_cost": 11800,
                    "customer_retention_rate": 86.5,
                },
                {
                    "year": 2007,
                    "revenue": 1680000,
                    "expenses": 1050000,
                    "profit": 630000,
                    "profitMargin": 37.5,
                    "employees": 58,
                    "customers": 26,
                    "marketShare": 2.4,
                    "productCount": 1,
                    "r_and_d_spending": 290000,
                    "marketing_spending": 210000,
                    "customer_acquisition_cost": 10900,
                    "customer_retention_rate": 87.2,
                },
                {
                    "year": 2008,
                    "revenue": 1820000,
                    "expenses": 1150000,
                    "profit": 670000,
                    "profitMargin": 36.8,
                    "employees": 65,
                    "customers": 42,
                    "marketShare": 3.5,
                    "productCount": 1,
                    "r_and_d_spending": 320000,
                    "marketing_spending": 230000,
                    "customer_acquisition_cost": 10200,
                    "customer_retention_rate": 88.0,
                },
                {
                    "year": 2009,
                    "revenue": 1950000,
                    "expenses": 1250000,
                    "profit": 700000,
                    "profitMargin": 35.9,
                    "employees": 72,
                    "customers": 68,
                    "marketShare": 4.2,
                    "productCount": 1,
                    "r_and_d_spending": 350000,
                    "marketing_spending": 260000,
                    "customer_acquisition_cost": 9800,
                    "customer_retention_rate": 89.1,
                },
                {
                    "year": 2010,
                    "revenue": 2100000,
                    "expenses": 1350000,
                    "profit": 750000,
                    "profitMargin": 35.7,
                    "employees": 80,
                    "customers": 95,
                    "marketShare": 5.0,
                    "productCount": 1,
                    "r_and_d_spending": 380000,
                    "marketing_spending": 290000,
                    "customer_acquisition_cost": 9500,
                    "customer_retention_rate": 89.8,
                },
                {
                    "year": 2011,
                    "revenue": 2250000,
                    "expenses": 1450000,
                    "profit": 800000,
                    "profitMargin": 35.5,
                    "employees": 88,
                    "customers": 125,
                    "marketShare": 5.6,
                    "productCount": 1,
                    "r_and_d_spending": 410000,
                    "marketing_spending": 320000,
                    "customer_acquisition_cost": 9200,
                    "customer_retention_rate": 90.2,
                },
                {
                    "year": 2012,
                    "revenue": 2400000,
                    "expenses": 1550000,
                    "profit": 850000,
                    "profitMargin": 35.4,
                    "employees": 95,
                    "customers": 168,
                    "marketShare": 6.3,
                    "productCount": 2,
                    "r_and_d_spending": 450000,
                    "marketing_spending": 350000,
                    "customer_acquisition_cost": 8900,
                    "customer_retention_rate": 90.5,
                },
                {
                    "year": 2013,
                    "revenue": 2550000,
                    "expenses": 1650000,
                    "profit": 900000,
                    "profitMargin": 35.2,
                    "employees": 102,
                    "customers": 210,
                    "marketShare": 6.8,
                    "productCount": 2,
                    "r_and_d_spending": 480000,
                    "marketing_spending": 380000,
                    "customer_acquisition_cost": 8600,
                    "customer_retention_rate": 90.8,
                },
                {
                    "year": 2014,
                    "revenue": 2700000,
                    "expenses": 1750000,
                    "profit": 950000,
                    "profitMargin": 35.1,
                    "employees": 110,
                    "customers": 256,
                    "marketShare": 7.4,
                    "productCount": 2,
                    "r_and_d_spending": 510000,
                    "marketing_spending": 410000,
                    "customer_acquisition_cost": 8300,
                    "customer_retention_rate": 91.0,
                },
                {
                    "year": 2015,
                    "revenue": 2850000,
                    "expenses": 1850000,
                    "profit": 1000000,
                    "profitMargin": 35.0,
                    "employees": 118,
                    "customers": 312,
                    "marketShare": 8.1,
                    "productCount": 2,
                    "r_and_d_spending": 540000,
                    "marketing_spending": 440000,
                    "customer_acquisition_cost": 8000,
                    "customer_retention_rate": 91.3,
                },
                {
                    "year": 2016,
                    "revenue": 3000000,
                    "expenses": 1950000,
                    "profit": 1050000,
                    "profitMargin": 35.0,
                    "employees": 125,
                    "customers": 380,
                    "marketShare": 8.9,
                    "productCount": 3,
                    "r_and_d_spending": 580000,
                    "marketing_spending": 480000,
                    "customer_acquisition_cost": 7700,
                    "customer_retention_rate": 91.6,
                },
                {
                    "year": 2017,
                    "revenue": 3150000,
                    "expenses": 2050000,
                    "profit": 1100000,
                    "profitMargin": 34.9,
                    "employees": 132,
                    "customers": 452,
                    "marketShare": 9.6,
                    "productCount": 3,
                    "r_and_d_spending": 620000,
                    "marketing_spending": 520000,
                    "customer_acquisition_cost": 7400,
                    "customer_retention_rate": 91.8,
                },
                {
                    "year": 2018,
                    "revenue": 3300000,
                    "expenses": 2150000,
                    "profit": 1150000,
                    "profitMargin": 34.8,
                    "employees": 140,
                    "customers": 528,
                    "marketShare": 10.3,
                    "productCount": 3,
                    "r_and_d_spending": 660000,
                    "marketing_spending": 560000,
                    "customer_acquisition_cost": 7100,
                    "customer_retention_rate": 92.0,
                },
                {
                    "year": 2019,
                    "revenue": 3450000,
                    "expenses": 2250000,
                    "profit": 1200000,
                    "profitMargin": 34.7,
                    "employees": 148,
                    "customers": 612,
                    "marketShare": 11.1,
                    "productCount": 4,
                    "r_and_d_spending": 710000,
                    "marketing_spending": 610000,
                    "customer_acquisition_cost": 6800,
                    "customer_retention_rate": 92.1,
                },
                {
                    "year": 2020,
                    "revenue": 3600000,
                    "expenses": 2350000,
                    "profit": 1250000,
                    "profitMargin": 34.7,
                    "employees": 155,
                    "customers": 725,
                    "marketShare": 12.5,
                    "productCount": 4,
                    "r_and_d_spending": 760000,
                    "marketing_spending": 660000,
                    "customer_acquisition_cost": 6500,
                    "customer_retention_rate": 92.2,
                },
                {
                    "year": 2021,
                    "revenue": 3750000,
                    "expenses": 2450000,
                    "profit": 1300000,
                    "profitMargin": 34.6,
                    "employees": 162,
                    "customers": 845,
                    "marketShare": 13.8,
                    "productCount": 4,
                    "r_and_d_spending": 810000,
                    "marketing_spending": 710000,
                    "customer_acquisition_cost": 6200,
                    "customer_retention_rate": 92.3,
                },
                {
                    "year": 2022,
                    "revenue": 3900000,
                    "expenses": 2550000,
                    "profit": 1350000,
                    "profitMargin": 34.6,
                    "employees": 170,
                    "customers": 980,
                    "marketShare": 15.2,
                    "productCount": 4,
                    "r_and_d_spending": 860000,
                    "marketing_spending": 760000,
                    "customer_acquisition_cost": 5900,
                    "customer_retention_rate": 92.4,
                },
                {
                    "year": 2023,
                    "revenue": 4050000,
                    "expenses": 2650000,
                    "profit": 1400000,
                    "profitMargin": 34.5,
                    "employees": 178,
                    "customers": 1120,
                    "marketShare": 16.4,
                    "productCount": 4,
                    "r_and_d_spending": 910000,
                    "marketing_spending": 810000,
                    "customer_acquisition_cost": 5600,
                    "customer_retention_rate": 92.4,
                },
                {
                    "year": 2024,
                    "revenue": 4200000,
                    "expenses": 2750000,
                    "profit": 1450000,
                    "profitMargin": 34.5,
                    "employees": 185,
                    "customers": 1265,
                    "marketShare": 17.6,
                    "productCount": 4,
                    "r_and_d_spending": 960000,
                    "marketing_spending": 860000,
                    "customer_acquisition_cost": 5300,
                    "customer_retention_rate": 92.5,
                },
                {
                    "year": 2025,
                    "revenue": 4350000,
                    "expenses": 2850000,
                    "profit": 1500000,
                    "profitMargin": 34.4,
                    "employees": 192,
                    "customers": 1420,
                    "marketShare": 18.3,
                    "productCount": 4,
                    "r_and_d_spending": 1010000,
                    "marketing_spending": 910000,
                    "customer_acquisition_cost": 5000,
                    "customer_retention_rate": 92.5,
                },
            ],
            "sustainabilityMetrics": {
                "carbonFootprint": {
                    "2020": 12500,
                    "2021": 11200,
                    "2022": 9800,
                    "2023": 8400,
                    "2024": 7200,
                    "2025Target": 6000,
                },
                "renewableEnergyUsage": {
                    "2020": 35,
                    "2021": 42,
                    "2022": 58,
                    "2023": 72,
                    "2024": 85,
                    "2025Target": 100,
                },
                "wasteReduction": {
                    "2020": 15,
                    "2021": 22,
                    "2022": 28,
                    "2023": 35,
                    "2024": 45,
                    "2025Target": 60,
                },
                "sustainabilityInitiatives": [
                    "Paperless Office Program",
                    "Remote Work Carbon Reduction",
                    "Sustainable Data Center Operations",
                    "Green Supply Chain Management",
                ],
            },
            "researchAndDevelopment": {
                "currentProjects": [
                    {
                        "name": "AI-Powered Business Analytics",
                        "startDate": "2023-03",
                        "completionTarget": "2024-Q2",
                        "budget": 1250000,
                        "teamSize": 18,
                        "status": "In Progress",
                    },
                    {
                        "name": "Blockchain Integration Platform",
                        "startDate": "2023-08",
                        "completionTarget": "2024-Q3",
                        "budget": 950000,
                        "teamSize": 12,
                        "status": "In Progress",
                    },
                    {
                        "name": "Low-Code Enterprise Solutions",
                        "startDate": "2023-11",
                        "completionTarget": "2024-Q4",
                        "budget": 820000,
                        "teamSize": 10,
                        "status": "Planning",
                    },
                ],
                "patents": {"filed": 48, "granted": 32, "pending": 16},
                "partnerships": [
                    {
                        "partner": "Stanford University",
                        "focus": "AI Research",
                        "startYear": 2021,
                    },
                    {"partner": "MIT", "focus": "Data Science", "startYear": 2022},
                    {
                        "partner": "ETH Zurich",
                        "focus": "Cybersecurity",
                        "startYear": 2023,
                    },
                ],
            },
        }
        self.design_system = """
           :root {
  --color-background: #292f33;
  --color-surface: #292f33;
  --color-text: #ffffff;
  --color-text-secondary: rgba(184, 196, 204, 0.7);
  --color-primary: #47e9ab;
  --color-primary-hover: #71f1c0;
  --color-primary-active: #a3ffdd;
  --color-secondary: rgba(86, 112, 128, 0.15);
  --color-secondary-hover: rgba(86, 112, 128, 0.25);
  --color-secondary-active: rgba(86, 112, 128, 0.3);
  --color-border: rgba(86, 112, 128, 0.3);
  --color-btn-primary-text: #292f33;
  --color-card-border: rgba(86, 112, 128, 0.2);
  --color-card-border-inner: rgba(86, 112, 128, 0.15);
  --color-error: #ff6915;
  --color-success: #47e9ab;
  --color-warning: #ffae00;
  --color-info: #b8c4cc;
  --color-focus-ring: rgba(71, 233, 171, 0.4);
  --color-select-caret: rgba(255, 255, 255, 0.8);
  --color-border-secondary: rgba(86, 112, 128, 0.2);

  /* Common style patterns */
  --focus-ring: 0 0 0 3px var(--color-focus-ring);
  --focus-outline: 2px solid var(--color-primary);
  --status-bg-opacity: 0.15;
  --status-border-opacity: 0.25;
  --select-caret-light: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23292F33' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  --select-caret-dark: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");

  /* RGB versions for opacity control */
  --color-success-rgb: 71, 233, 171;
  --color-error-rgb: 255, 105, 21;
  --color-warning-rgb: 255, 174, 0;
  --color-info-rgb: 184, 196, 204;

  /* Typography */
  --font-family-base: "FKGroteskNeue", "Geist", "Inter", -apple-system,
    BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-family-mono: "Berkeley Mono", ui-monospace, SFMono-Regular, Menlo,
    Monaco, Consolas, monospace;
  --font-size-xs: 11px;
  --font-size-sm: 12px;
  --font-size-base: 14px;
  --font-size-md: 14px;
  --font-size-lg: 16px;
  --font-size-xl: 18px;
  --font-size-2xl: 20px;
  --font-size-3xl: 24px;
  --font-size-4xl: 30px;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 550;
  --font-weight-bold: 600;
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --letter-spacing-tight: -0.01em;

  /* Spacing */
  --space-0: 0;
  --space-1: 1px;
  --space-2: 2px;
  --space-4: 4px;
  --space-6: 6px;
  --space-8: 8px;
  --space-10: 10px;
  --space-12: 12px;
  --space-16: 16px;
  --space-20: 20px;
  --space-24: 24px;
  --space-32: 32px;

  /* Border Radius */
  --radius-sm: 6px;
  --radius-base: 8px;
  --radius-md: 10px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.02);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.04),
    0 2px 4px -1px rgba(0, 0, 0, 0.02);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.04),
    0 4px 6px -2px rgba(0, 0, 0, 0.02);
  --shadow-inset-sm: inset 0 1px 0 rgba(255, 255, 255, 0.1),
    inset 0 -1px 0 rgba(0, 0, 0, 0.15);

  /* Animation */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --ease-standard: cubic-bezier(0.16, 1, 0.3, 1);

  /* Layout */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
}

/* Base styles */
html {
  font-size: var(--font-size-base);
  font-family: var(--font-family-base);
  line-height: var(--line-height-normal);
  color: var(--color-text);
  background-color: var(--color-background);
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
}

*,
*::before,
*::after {
  box-sizing: inherit;
}

/* Typography */
h1,
h2,
h3,
h4,
h5,
h6 {
  margin: 0;
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);
  color: var(--color-text);
  letter-spacing: var(--letter-spacing-tight);
}

h1 {
  font-size: var(--font-size-4xl);
}
h2 {
  font-size: var(--font-size-3xl);
}
h3 {
  font-size: var(--font-size-2xl);
}
h4 {
  font-size: var(--font-size-xl);
}
h5 {
  font-size: var(--font-size-lg);
}
h6 {
  font-size: var(--font-size-md);
}

p {
  margin: 0 0 var(--space-16) 0;
}

a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--duration-fast) var(--ease-standard);
}

a:hover {
  color: var(--color-primary-hover);
}

code,
pre {
  font-family: var(--font-family-mono);
  font-size: calc(var(--font-size-base) * 0.95);
  background-color: var(--color-secondary);
  border-radius: var(--radius-sm);
}

code {
  padding: var(--space-1) var(--space-4);
}

pre {
  padding: var(--space-16);
  margin: var(--space-16) 0;
  overflow: auto;
  border: 1px solid var(--color-border);
}

pre code {
  background: none;
  padding: 0;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-8) var(--space-16);
  border-radius: var(--radius-base);
  font-size: var(--font-size-base);
  font-weight: 500;
  line-height: 1.5;
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-standard);
  border: none;
  text-decoration: none;
  position: relative;
}

.btn:focus-visible {
  outline: none;
  box-shadow: var(--focus-ring);
}

.btn--primary {
  background: var(--color-primary);
  color: var(--color-btn-primary-text);
}

.btn--primary:hover {
  background: var(--color-primary-hover);
}

.btn--primary:active {
  background: var(--color-primary-active);
}

.btn--secondary {
  background: var(--color-secondary);
  color: var(--color-text);
}

.btn--secondary:hover {
  background: var(--color-secondary-hover);
}

.btn--secondary:active {
  background: var(--color-secondary-active);
}

.btn--outline {
  background: transparent;
  border: 1px solid var(--color-border-secondary);
  color: var(--color-text);
}

.btn--outline:hover {
  background: var(--color-secondary);
}

.btn--sm {
  padding: var(--space-4) var(--space-12);
  font-size: var(--font-size-sm);
  border-radius: var(--radius-sm);
}

.btn--lg {
  padding: var(--space-10) var(--space-20);
  font-size: var(--font-size-lg);
  border-radius: var(--radius-md);
}

.btn--full-width {
  width: 100%;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Form elements */
.form-control {
  display: block;
  width: 100%;
  padding: var(--space-8) var(--space-12);
  font-size: var(--font-size-md);
  line-height: 1.5;
  color: var(--color-text);
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-base);
  transition: border-color var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard);
}

textarea.form-control {
  font-family: var(--font-family-base);
  font-size: var(--font-size-base);
}

select.form-control {
  padding: var(--space-8) var(--space-12);
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: var(--select-caret-dark);
  background-repeat: no-repeat;
  background-position: right var(--space-12) center;
  background-size: 16px;
  padding-right: var(--space-32);
}

.form-control:focus {
  border-color: var(--color-primary);
  outline: var(--focus-outline);
}

.form-label {
  display: block;
  margin-bottom: var(--space-8);
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-sm);
}

.form-group {
  margin-bottom: var(--space-16);
}

/* Card component */
.card {
  background-color: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-card-border);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: box-shadow var(--duration-normal) var(--ease-standard);
}

.card:hover {
  box-shadow: var(--shadow-md);
}

.card__body {
  padding: var(--space-16);
}

.card__header,
.card__footer {
  padding: var(--space-16);
  border-bottom: 1px solid var(--color-card-border-inner);
}

/* Status indicators - simplified with CSS variables */
.status {
  display: inline-flex;
  align-items: center;
  padding: var(--space-6) var(--space-12);
  border-radius: var(--radius-full);
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-sm);
}

.status--success {
  background-color: rgba(
    var(--color-success-rgb, 33, 128, 141),
    var(--status-bg-opacity)
  );
  color: var(--color-success);
  border: 1px solid
    rgba(var(--color-success-rgb, 33, 128, 141), var(--status-border-opacity));
}

.status--error {
  background-color: rgba(
    var(--color-error-rgb, 192, 21, 47),
    var(--status-bg-opacity)
  );
  color: var(--color-error);
  border: 1px solid
    rgba(var(--color-error-rgb, 192, 21, 47), var(--status-border-opacity));
}

.status--warning {
  background-color: rgba(
    var(--color-warning-rgb, 168, 75, 47),
    var(--status-bg-opacity)
  );
  color: var(--color-warning);
  border: 1px solid
    rgba(var(--color-warning-rgb, 168, 75, 47), var(--status-border-opacity));
}

.status--info {
  background-color: rgba(
    var(--color-info-rgb, 98, 108, 113),
    var(--status-bg-opacity)
  );
  color: var(--color-info);
  border: 1px solid
    rgba(var(--color-info-rgb, 98, 108, 113), var(--status-border-opacity));
}

/* Container layout */
.container {
  width: 100%;
  margin-right: auto;
  margin-left: auto;
  padding-right: var(--space-16);
  padding-left: var(--space-16);
}

@media (min-width: 640px) {
  .container {
    max-width: var(--container-sm);
  }
}
@media (min-width: 768px) {
  .container {
    max-width: var(--container-md);
  }
}
@media (min-width: 1024px) {
  .container {
    max-width: var(--container-lg);
  }
}
@media (min-width: 1280px) {
  .container {
    max-width: var(--container-xl);
  }
}

/* Utility classes */
.flex {
  display: flex;
}
.flex-col {
  flex-direction: column;
}
.items-center {
  align-items: center;
}
.justify-center {
  justify-content: center;
}
.justify-between {
  justify-content: space-between;
}
.gap-4 {
  gap: var(--space-4);
}
.gap-8 {
  gap: var(--space-8);
}
.gap-16 {
  gap: var(--space-16);
}

.m-0 {
  margin: 0;
}
.mt-8 {
  margin-top: var(--space-8);
}
.mb-8 {
  margin-bottom: var(--space-8);
}
.mx-8 {
  margin-left: var(--space-8);
  margin-right: var(--space-8);
}
.my-8 {
  margin-top: var(--space-8);
  margin-bottom: var(--space-8);
}

.p-0 {
  padding: 0;
}
.py-8 {
  padding-top: var(--space-8);
  padding-bottom: var(--space-8);
}
.px-8 {
  padding-left: var(--space-8);
  padding-right: var(--space-8);
}
.py-16 {
  padding-top: var(--space-16);
  padding-bottom: var(--space-16);
}
.px-16 {
  padding-left: var(--space-16);
  padding-right: var(--space-16);
}

.block {
  display: block;
}
.hidden {
  display: none;
}

/* Accessibility */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

:focus-visible {
  outline: var(--focus-outline);
  outline-offset: 2px;
}

@font-face {
  font-family: "FKGroteskNeue";
  src: url("https://www.perplexity.ai/fonts/FKGroteskNeue.woff2")
    format("woff2");
}

/* Dashboard specific styles */
.dashboard-container {
  min-height: 100vh;
  background-color: var(--color-background);
}

.dashboard-header {
  background-color: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-16) 0;
  box-shadow: var(--shadow-sm);
}

.logo-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.logo-text {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  margin: 0;
}

.logo-subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
}

.header-actions {
  display: flex;
  gap: var(--space-12);
  align-items: center;
}

/* Stats Section */
.stats-section {
  padding: var(--space-32) 0;
  background-color: var(--color-surface);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-24);
}

.stat-card {
  background-color: var(--color-background);
  padding: var(--space-24);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-card-border);
  text-align: center;
  box-shadow: var(--shadow-sm);
  transition: transform var(--duration-fast) var(--ease-standard);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-value {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  margin-bottom: var(--space-8);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
}

/* Main Content Layout */
.main-content {
  padding: var(--space-32) 0;
}

.content-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: var(--space-32);
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: var(--space-24);
  }
}

/* Filters Sidebar */
.filters-sidebar {
  display: flex;
  flex-direction: column;
  gap: var(--space-24);
}

.filter-section {
  background-color: var(--color-surface);
  padding: var(--space-20);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-card-border);
  box-shadow: var(--shadow-sm);
}

.filter-section h3 {
  margin-bottom: var(--space-16);
  font-size: var(--font-size-lg);
  color: var(--color-text);
}

.analytics-section {
  background-color: var(--color-surface);
  padding: var(--space-20);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-card-border);
  box-shadow: var(--shadow-sm);
}

.analytics-section h3 {
  margin-bottom: var(--space-16);
  font-size: var(--font-size-lg);
  color: var(--color-text);
}

.chart-container {
  margin-bottom: var(--space-20);
  position: relative;
  height: 220px;
  width: 100%;
}

.chart-container:last-child {
  margin-bottom: 0;
}

.chart-title {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-8);
  text-align: center;
}

.chart-container canvas {
  max-height: 200px !important;
  max-width: 100% !important;
}

/* Companies Content */
.companies-content {
  background-color: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-card-border);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.content-header {
  padding: var(--space-20);
  border-bottom: 1px solid var(--color-card-border-inner);
  background-color: var(--color-background);
}

.content-header h2 {
  margin: 0;
  font-size: var(--font-size-xl);
  color: var(--color-text);
}

.view-controls {
  display: flex;
  gap: var(--space-12);
  align-items: center;
}

.view-controls .form-control {
  min-width: 180px;
}

/* Companies Grid */
.companies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: var(--space-16);
  padding: var(--space-20);
}

@media (max-width: 768px) {
  .companies-grid {
    grid-template-columns: 1fr;
  }
}

.company-card {
  background-color: var(--color-background);
  border: 1px solid var(--color-card-border);
  border-radius: var(--radius-base);
  padding: var(--space-16);
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-standard);
}

.company-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary);
}

.company-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-12);
}

.company-name {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin: 0;
}

.company-stage {
  padding: var(--space-4) var(--space-8);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stage-seed {
  background-color: rgba(var(--color-info-rgb), 0.15);
  color: var(--color-info);
  border: 1px solid rgba(var(--color-info-rgb), 0.25);
}

.stage-series-a {
  background-color: rgba(var(--color-warning-rgb), 0.15);
  color: var(--color-warning);
  border: 1px solid rgba(var(--color-warning-rgb), 0.25);
}

.stage-series-b,
.stage-series-d {
  background-color: rgba(var(--color-success-rgb), 0.15);
  color: var(--color-success);
  border: 1px solid rgba(var(--color-success-rgb), 0.25);
}

.stage-pre-seed {
  background-color: rgba(var(--color-text-secondary), 0.15);
  color: var(--color-text-secondary);
  border: 1px solid rgba(var(--color-text-secondary), 0.25);
}

.company-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--font-size-sm);
}

.info-label {
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
}

.info-value {
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
  text-align: right;
}

.company-description {
  margin-top: var(--space-12);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.company-footer {
  margin-top: var(--space-12);
  padding-top: var(--space-12);
  border-top: 1px solid var(--color-card-border-inner);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ceo-info {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.ceo-name {
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
}

.view-details {
  font-size: var(--font-size-sm);
  color: var(--color-primary);
  font-weight: var(--font-weight-medium);
  text-decoration: none;
}

.view-details:hover {
  color: var(--color-primary-hover);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--space-20);
}

.modal-overlay.active {
  display: flex;
}

.modal-content {
  background-color: var(--color-surface);
  border-radius: var(--radius-lg);
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-24);
  border-bottom: 1px solid var(--color-card-border-inner);
  position: sticky;
  top: 0;
  background-color: var(--color-surface);
  z-index: 1;
}

.modal-header h2 {
  margin: 0;
  font-size: var(--font-size-2xl);
  color: var(--color-text);
}

.modal-close {
  background: none;
  border: none;
  font-size: var(--font-size-2xl);
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  transition: all var(--duration-fast) var(--ease-standard);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  background-color: var(--color-secondary);
  color: var(--color-text);
}

.modal-body {
  padding: var(--space-24);
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-32);
}

@media (max-width: 768px) {
  .modal-grid {
    grid-template-columns: 1fr;
    gap: var(--space-24);
  }
}

.modal-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-16);
}

.modal-section.contact-section {
  grid-column: 1 / -1;
}

.modal-section h3 {
  margin: 0 0 var(--space-12) 0;
  font-size: var(--font-size-lg);
  color: var(--color-text);
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: var(--space-8);
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.detail-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-value {
  font-size: var(--font-size-base);
  color: var(--color-text);
  line-height: 1.4;
}

.detail-value.link {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--duration-fast) var(--ease-standard);
}

.detail-value.link:hover {
  color: var(--color-primary-hover);
  text-decoration: underline;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: var(--space-32);
  color: var(--color-text-secondary);
  grid-column: 1 / -1;
}

.empty-state h3 {
  margin-bottom: var(--space-8);
  color: var(--color-text);
}

/* Loading State */
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--space-32);
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
}

/* Enhanced Data Visualization Cards */
.data-insight-card {
  background: linear-gradient(
    135deg,
    var(--color-primary) 0%,
    rgba(33, 128, 141, 0.8) 100%
  );
  color: white;
  border-radius: var(--radius-lg);
  padding: var(--space-24);
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(33, 128, 141, 0.3);
  transition: all var(--duration-normal) var(--ease-standard);
}

.data-insight-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 70%
  );
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.data-insight-card:hover::before {
  transform: translateX(100%);
}

.data-insight-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 48px rgba(33, 128, 141, 0.4);
}

/* Enhanced Metric Cards with Progress Indicators */
.metric-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-24);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--color-card-border);
  position: relative;
  overflow: hidden;
  transition: all var(--duration-normal) var(--ease-standard);
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.metric-value-large {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  margin-bottom: var(--space-8);
  line-height: 1.1;
}

.metric-trend {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  margin-top: var(--space-8);
}

.metric-trend.positive {
  color: var(--color-success);
}

.metric-trend.negative {
  color: var(--color-error);
}

.metric-trend::before {
  content: "";
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
}

.metric-trend.positive::before {
  border-bottom: 6px solid var(--color-success);
}

.metric-trend.negative::before {
  border-top: 6px solid var(--color-error);
}

/* Progress Bar Components */
.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--color-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
  margin-top: var(--space-12);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(
    90deg,
    var(--color-primary) 0%,
    var(--color-primary-hover) 100%
  );
  border-radius: var(--radius-full);
  transition: width 1s ease-out;
  position: relative;
}

.progress-fill::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 70%
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Enhanced Company Cards with Rich Information Display */
.company-card-enhanced {
  background: var(--color-surface);
  border: 1px solid var(--color-card-border);
  border-radius: var(--radius-lg);
  padding: var(--space-20);
  position: relative;
  overflow: hidden;
  transition: all var(--duration-normal) var(--ease-standard);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.company-card-enhanced::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(
    180deg,
    var(--color-primary) 0%,
    var(--color-primary-hover) 100%
  );
  transform: scaleY(0);
  transition: transform var(--duration-normal) var(--ease-standard);
}

.company-card-enhanced:hover::before {
  transform: scaleY(1);
}

.company-card-enhanced:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  border-color: var(--color-primary);
}

.company-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: var(--space-16);
  margin-top: var(--space-16);
}

.company-metric {
  text-align: center;
  padding: var(--space-12);
  background: var(--color-background);
  border-radius: var(--radius-base);
  border: 1px solid var(--color-card-border);
}

.company-metric-value {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  margin-bottom: var(--space-4);
}

.company-metric-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Enhanced Chart Containers */
.chart-container-enhanced {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-20);
  border: 1px solid var(--color-card-border);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
  margin-bottom: var(--space-24);
}

.chart-container-enhanced::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(
    90deg,
    var(--color-primary) 0%,
    var(--color-primary-hover) 100%
  );
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-16);
  padding-bottom: var(--space-12);
  border-bottom: 1px solid var(--color-card-border);
}

.chart-title-enhanced {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin: 0;
}

.chart-subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-top: var(--space-4);
}

.chart-actions {
  display: flex;
  gap: var(--space-8);
}

.chart-action-btn {
  padding: var(--space-4) var(--space-8);
  border: 1px solid var(--color-border);
  background: var(--color-background);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-standard);
}

.chart-action-btn:hover {
  background: var(--color-secondary);
  border-color: var(--color-primary);
}

.chart-action-btn.active {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

/* Financial Metrics Display */
.financial-overview {
  background: linear-gradient(
    135deg,
    var(--color-success) 0%,
    rgba(50, 184, 198, 0.9) 100%
  );
  color: white;
  padding: var(--space-32);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-24);
  position: relative;
  overflow: hidden;
}

.financial-overview::before {
  content: "";
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.1) 0%,
    transparent 70%
  );
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.financial-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-24);
  position: relative;
  z-index: 1;
}

.financial-item {
  text-align: center;
}

.financial-value {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--space-8);
}

.financial-label {
  font-size: var(--font-size-base);
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Enhanced Filter Sidebar */
.filter-section-enhanced {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-20);
  border: 1px solid var(--color-card-border);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
  margin-bottom: var(--space-20);
}

.filter-section-enhanced::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(
    90deg,
    var(--color-primary) 0%,
    var(--color-primary-hover) 100%
  );
}

.filter-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-16);
  color: var(--color-text);
  position: relative;
  padding-bottom: var(--space-8);
}

.filter-title::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 30px;
  height: 2px;
  background: var(--color-primary);
}

/* Enhanced Form Controls */
.form-control-enhanced {
  background: var(--color-surface);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-base);
  padding: var(--space-12) var(--space-16);
  font-size: var(--font-size-base);
  transition: all var(--duration-normal) var(--ease-standard);
  position: relative;
}

.form-control-enhanced:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(33, 128, 141, 0.1);
  outline: none;
}

.form-control-enhanced:hover {
  border-color: var(--color-primary);
}

/* Data Visualization Enhancements */
.data-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-20);
  margin-top: var(--space-24);
}

.data-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-20);
  border: 1px solid var(--color-card-border);
  transition: all var(--duration-normal) var(--ease-standard);
  position: relative;
  overflow: hidden;
}

.data-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(
    90deg,
    var(--color-primary) 0%,
    var(--color-success) 100%
  );
  transform: scaleX(0);
  transition: transform var(--duration-normal) var(--ease-standard);
}

.data-card:hover::before {
  transform: scaleX(1);
}

.data-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.data-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-16);
}

.data-card-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin: 0;
}

.data-card-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(
    135deg,
    var(--color-primary) 0%,
    var(--color-primary-hover) 100%
  );
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: var(--font-weight-bold);
}

/* Animation Utilities */
@keyframes slideInUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-slide-in {
  animation: slideInUp 0.6s ease-out;
}

.animate-fade-in {
  animation: fadeIn 0.4s ease-out;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .dashboard-header .container {
    flex-direction: column;
    gap: var(--space-16);
    text-align: center;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-16);
  }

  .content-header {
    flex-direction: column;
    gap: var(--space-12);
    align-items: flex-start;
  }

  .view-controls .form-control {
    min-width: auto;
    width: 100%;
  }

  .modal-content {
    margin: var(--space-12);
    max-height: calc(100vh - 24px);
  }

  .chart-container {
    height: 180px;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .filters-sidebar {
    order: 2;
  }

  .companies-content {
    order: 1;
  }

  .financial-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-16);
  }

  .data-grid {
    grid-template-columns: 1fr;
  }

  .company-metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .companies-grid {
    padding: var(--space-12);
    gap: var(--space-12);
  }

  .company-card {
    padding: var(--space-12);
  }

  .modal-body {
    padding: var(--space-16);
  }

  .modal-header {
    padding: var(--space-16);
  }

  .financial-grid {
    grid-template-columns: 1fr;
  }

  .metric-value-large {
    font-size: clamp(1.5rem, 4vw, 2.5rem);
  }
}

/* Advanced Data Visualization Components */

/* Sparkline Charts */
.sparkline-container {
  position: relative;
  height: 60px;
  width: 100%;
  margin-top: var(--space-12);
}

.sparkline-svg {
  width: 100%;
  height: 100%;
  overflow: visible;
}

.sparkline-path {
  fill: none;
  stroke: var(--color-primary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.sparkline-area {
  fill: url(#sparklineGradient);
  opacity: 0.3;
}

/* Donut Chart Component */
.donut-chart-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: var(--space-20) 0;
}

.donut-chart {
  transform: rotate(-90deg);
}

.donut-chart-center {
  position: absolute;
  text-align: center;
}

.donut-chart-value {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  line-height: 1;
}

.donut-chart-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-top: var(--space-4);
}

/* Enhanced Table Styles */
.data-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.data-table th,
.data-table td {
  padding: var(--space-16);
  text-align: left;
  border-bottom: 1px solid var(--color-card-border);
}

.data-table th {
  background: var(--color-background);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  font-size: var(--font-size-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.data-table tr:hover {
  background: var(--color-secondary);
}

.data-table tr:last-child td {
  border-bottom: none;
}

/* Performance Indicator */
.performance-indicator {
  display: inline-flex;
  align-items: center;
  gap: var(--space-8);
  padding: var(--space-8) var(--space-12);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.performance-indicator.excellent {
  background: rgba(var(--color-success-rgb), 0.15);
  color: var(--color-success);
}

.performance-indicator.good {
  background: rgba(var(--color-info-rgb), 0.15);
  color: var(--color-info);
}

.performance-indicator.average {
  background: rgba(var(--color-warning-rgb), 0.15);
  color: var(--color-warning);
}

.performance-indicator.poor {
  background: rgba(var(--color-error-rgb), 0.15);
  color: var(--color-error);
}

.performance-indicator::before {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

/* Time Series Chart Enhancement */
.time-series-container {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-24);
  border: 1px solid var(--color-card-border);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  margin-bottom: var(--space-24);
}

.time-series-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-20);
}

.time-range-selector {
  display: flex;
  gap: var(--space-4);
  background: var(--color-background);
  border-radius: var(--radius-base);
  padding: var(--space-4);
  border: 1px solid var(--color-card-border);
}

.time-range-btn {
  padding: var(--space-6) var(--space-12);
  border: none;
  background: transparent;
  font-size: var(--font-size-sm);
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: all var(--duration-fast) var(--ease-standard);
}

.time-range-btn:hover {
  background: var(--color-secondary);
}

.time-range-btn.active {
  background: var(--color-primary);
  color: white;
}

/* KPI Dashboard Grid */
.kpi-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-20);
  margin-bottom: var(--space-32);
}

.kpi-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-20);
  border: 1px solid var(--color-card-border);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: all var(--duration-normal) var(--ease-standard);
  position: relative;
  overflow: hidden;
}

.kpi-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(
    90deg,
    var(--color-primary) 0%,
    var(--color-success) 100%
  );
  transform: scaleX(0);
  transition: transform var(--duration-normal) var(--ease-standard);
}

.kpi-card:hover::before {
  transform: scaleX(1);
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-16);
}

.kpi-title {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  margin: 0;
}

.kpi-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(
    135deg,
    var(--color-primary) 0%,
    var(--color-primary-hover) 100%
  );
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-bold);
}

.kpi-value {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin-bottom: var(--space-8);
  line-height: 1.1;
}

.kpi-change {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.kpi-change.positive {
  color: var(--color-success);
}

.kpi-change.negative {
  color: var(--color-error);
}

.kpi-change::before {
  content: "";
  width: 0;
  height: 0;
  border-left: 3px solid transparent;
  border-right: 3px solid transparent;
}

.kpi-change.positive::before {
  border-bottom: 5px solid var(--color-success);
}

.kpi-change.negative::before {
  border-top: 5px solid var(--color-error);
}

/* Enhanced Filter Panel */
.filter-panel {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-24);
  border: 1px solid var(--color-card-border);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: var(--space-24);
}

.filter-group {
  margin-bottom: var(--space-24);
}

.filter-group:last-child {
  margin-bottom: 0;
}

.filter-group-title {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin-bottom: var(--space-12);
  display: flex;
  align-items: center;
  gap: var(--space-8);
}

.filter-group-title::before {
  content: "";
  width: 3px;
  height: 16px;
  background: var(--color-primary);
  border-radius: var(--radius-sm);
}

.filter-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: var(--space-8);
  cursor: pointer;
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  transition: background-color var(--duration-fast) var(--ease-standard);
}

.filter-checkbox:hover {
  background: var(--color-secondary);
}

.filter-checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  margin: 0;
  cursor: pointer;
}

.filter-checkbox label {
  font-size: var(--font-size-sm);
  color: var(--color-text);
  cursor: pointer;
  margin: 0;
}

/* Loading States */
.loading-skeleton {
  background: linear-gradient(
    90deg,
    var(--color-secondary) 25%,
    rgba(255, 255, 255, 0.5) 50%,
    var(--color-secondary) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: var(--radius-base);
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.skeleton-text {
  height: 1em;
  margin-bottom: var(--space-8);
}

.skeleton-title {
  height: 1.5em;
  width: 60%;
  margin-bottom: var(--space-12);
}

.skeleton-card {
  height: 200px;
  border-radius: var(--radius-lg);
}

/* Interactive Elements */
.interactive-element {
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-standard);
}

.interactive-element:hover {
  transform: scale(1.02);
}

.interactive-element:active {
  transform: scale(0.98);
}

/* Tooltip Enhancement */
.tooltip {
  position: relative;
  cursor: help;
}

.tooltip::before {
  content: attr(data-tooltip);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-text);
  color: var(--color-background);
  padding: var(--space-8) var(--space-12);
  border-radius: var(--radius-base);
  font-size: var(--font-size-sm);
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all var(--duration-fast) var(--ease-standard);
  z-index: 1000;
}

.tooltip::after {
  content: "";
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid var(--color-text);
  opacity: 0;
  visibility: hidden;
  transition: all var(--duration-fast) var(--ease-standard);
}

.tooltip:hover::before,
.tooltip:hover::after {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) translateY(-4px);
}

/* Notification System */
.notification {
  position: fixed;
  top: var(--space-20);
  right: var(--space-20);
  max-width: 400px;
  background: var(--color-surface);
  border-radius: var(--radius-base);
  padding: var(--space-16);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border-left: 4px solid var(--color-primary);
  z-index: 1000;
  animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification.success {
  border-left-color: var(--color-success);
}

.notification.error {
  border-left-color: var(--color-error);
}

.notification.warning {
  border-left-color: var(--color-warning);
}

.notification-title {
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-4);
  color: var(--color-text);
}

.notification-message {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: 1.4;
}
        """

    async def generate_dashboard(self, request: RequestSchema):
        try:
            config = RunnableConfig(configurable={"thread_id": "1"})

            initial_state: AgentState = {
                "query": request.query,
                "data": self.data,
                "design_system": self.design_system,
            }

            response = await self.agent.graph.ainvoke(initial_state, config=config)
            html = response["html"]
            js = response["js"]
            js_utils = response["js_utils"]

            files_obj = {
                "page_title": "",
                "html": html,
                "js_utils": js_utils,
                "js": js,
            }

            hosted_url = await self.r2.upload_to_storage(files_obj)

            return ResponseSchema(url=hosted_url)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Dashboard generation service failed: {e}"
            )
