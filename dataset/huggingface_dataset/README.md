---
annotations_creators:
- expert-generated
language:
- en
language_creators:
- expert-generated
license:
- mit
multilinguality:
- monolingual
pretty_name: AI Search Providers Benchmark Dataset
size_categories:
- 100<n<1K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
tags:
- search
- factual-accuracy
- news
- knowledge
---

# AI Search Providers Benchmark Dataset

## 📚 Introduction

This dataset is designed for benchmarking AI-powered search engines, including:

1. Datura (Meta - Bittensor Network, Subnet 22)
2. You.com
3. OpenAI ChatGPT
4. Perplexity
5. Google Gemini
6. Andi Search
7. X Grok

## 📊 Dataset Structure

Each entry contains:
- `id`: Unique identifier for the QA pair
- `question`: The query text
- `expected_answer`: The correct answer
- `category`: Topic category
- `area`: Broader area classification (News/Knowledge)

## 🎯 Categories

The dataset covers various domains including:
- Entertainment
- Sports
- Technology
- General News
- Finance
- Architecture
- Arts
- Astronomy
- Auto (Automotive)
- E-sports
- Fashion
- False Premise

## 📈 Dataset Characteristics

The dataset is categorized into four major types:

1. **Simple**: Basic questions requiring minimal analysis
2. **Complex**: Questions needing synthesis across multiple sources
3. **Hallucination Inducing**: Questions with false premises to test AI's factual accuracy
4. **News**: Questions with answers that change due to recent developments

## 🔍 Use Cases

This dataset is particularly useful for:
- Evaluating search engine accuracy and relevance
- Testing false premise detection capabilities
- Assessing topic classification accuracy
- Benchmarking question-answering systems
- Measuring response quality and factual accuracy
- Testing handling of time-sensitive information

## 🛠️ Methodology

The dataset was created by:
1. Scraping various trustworthy sources for interesting facts and lessons
2. Creating sets of Q&A to represent those facts
3. Adjusting the tone, style, and distribution of queries to match production users

## 📊 Dataset Statistics

The dataset includes a diverse range of questions and answers, with special attention to:
- Current events and news
- Technical and scientific topics
- Entertainment and sports
- Historical facts
- Common misconceptions and false premises

This comprehensive coverage ensures the dataset is suitable for evaluating various aspects of AI search capabilities.