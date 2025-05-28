# Animora SEO Article Generation System

![animora-blog](/images/animora-blog.png)

Automated end-to-end system that **crawls, writes, audits, and publishes SEO-optimised articles** for the pet-photo SNS **Animora**. \
Written in **Python** and provisioned on **Azure** with **Terraform**, the pipeline demonstrates production-grade MLOps / LLMOps practices.

## Technologies Used
<p style="display: inline">
    <img src=https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge>
    <img src="https://img.shields.io/badge/-Azure-0089D6.svg?logo=azure-devops&logoColor=white&style=for-the-badge" />
  <img src="https://img.shields.io/badge/-Terraform-5C4EE5.svg?logo=terraform&logoColor=white&style=for-the-badge" />
    <img src=https://img.shields.io/badge/-OpenAI-412991.svg?logo=openai&style=for-the-badge>
    <img src="https://img.shields.io/badge/-Google_Search-4285F4.svg?logo=google&logoColor=white&style=for-the-badge" />
    <img src="https://img.shields.io/badge/-Lighthouse-28A745.svg?logo=googlechrome&logoColor=white&style=for-the-badge" />
</p>

## Key Features
- **Web Crawling & Data Collection**: Uses Google SERP to scrape top 10 articles' titles, H2 headings, and content. (`s01_web_crawler`)

- **RAG Indexing**: Indexes scraped data into Azure AI Search for retrieval-augmented generation. (`s02_rag_indexer`)

- **Outline & Draft Generation**: Generates article outlines and full drafts via Azure OpenAI (GPT) with guardrails to ensure factual accuracy. (`s03_draft_generator`)

- **Automated Image Selection**: Fetches relevant images from Unsplash, Pexels, and Pixabay; filters by semantic similarity. (`s04_image_picker`)

- **SEO Auditing**: Evaluates articles using Google Lighthouse, checks keyword density, and generates meta tags. (`s05_seo_auditor`)

- **Automated Publishing**: Converts content to MDX format and deploys to the website repository. (`s06_publisher`)

## Repository Structure
```
.
├── functions
│   ├── __init__.py
│   ├── activities
│   │   ├── s01_web_crawler
│   │   ├── s02_rag_indexer
│   │   ├── s03_draft_generator
│   │   ├── s04_image_picker
│   │   ├── s05_seo_auditor
│   │   └── s06_publisher
│   ├── config
│   │   ├── __init__.py
│   │   ├── get_refresh_token.py
│   │   ├── prompts.py
│   │   └── settings.py
│   ├── function_app.py
│   ├── host.json
│   ├── orchestrator
│   │   ├── __init__.py
│   │   ├── activities.py
│   │   ├── orchestrator.py
│   │   └── starter.py
│   └── utils
├── infra
│   ├── envs
│   │   └── backend.tfvars
│   ├── main.tf
│   ├── modules
│   │   ├── cognitive
│   │   ├── function
│   │   ├── keyvault
│   │   ├── monitoring
│   │   ├── rg
│   │   └── search
│   ├── outputs.tf
│   ├── README.md
│   ├── terraform.tfvars
│   ├── variables.tf
│   └── versions.tf
└── README.md
```
## Getting Started
1. **Clone the repository**:

    ```bash
    git clone git@github.com:Shunta6855/animora-seo.git
    cd animora-seo
    ```

2. Create a remote backend Storage Account and container

    ```bash
    # Login to Azure Service
    az login

    # Set your Azure subscription ID
    export ARM_SUBSCRIPTION_ID="<your-subscription-id>"

    # Create Resource Group
    az group create --name <your-resource-group> --location japaneast

    # Create Storage Account
    az storage account create \
    --name <yourstorageaccountname> \
    --resource-group <your-resource-group> \
    --location japaneast \
    --sku Standard_LRS \
    --encryption-services blob

    # Create Blob Container
    az storage container create \
    --name tfstate \
    --account-name <yourstorageaccountname> \
    --auth-mode login
    ```

3. Define Azure AI Search index for RAG

4. Configure Terraform
    ```
    cd infra
    terraform init 
    terraform plan
    terraform apply
    ``` 

5. Set environment variables with local.settings.json using .env.example

6. Setup Azurite (Local Emulator)
    ```bash
    azurite --silent --location /tmp/azurite --debug /tmp/azurite/debug.log
    ```

7. Run the orchestrator locally
    ```bash
    cd funcitons
    func start
    ```