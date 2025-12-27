graph TD
A[User Upload Resume] --> B[Extract Text]
B --> C[Parse Resume]
C --> D{JD Provided?}
D -->|No| E[Auto Generate JD]
D -->|Yes| F[Use Provided JD]
E --> G[ATS Scoring Engine]
F --> G
G --> H{ATS >= 80?}
H -->|No| I[Enhance Resume]
I --> G
H -->|Yes| J[Template Selection Agent]
J --> K[LaTeX Builder]
K --> L[PDF Generator]
