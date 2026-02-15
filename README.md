# Semantic-Commerce-Analyzer
This suite uses Computer Vision (OpenCLIP) and Natural Language Processing (TF-IDF) to identify cross-modal item correlations and detect near-duplicate listings on e-commerce platform

**Key Features**
Asynchronous Web Extraction: Scraping engine with advanced anti-bot evasion techniques (CDP commands, dynamic user-agent rotation).

🔍**Case Study**

**Carousell Analysis**

This project implements a pre-configured scraper and parser for Carousell, demonstrating the framework's capability to:
1. Handle Dynamic SPAs: Successfully extracting data from single-page applications.
2. Bypass Bot Mitigation: Use undetected-chromedriver and custom header rotation to operate within high-security environments like Cloudflare.
3. Analyze Real-World Data: Processing diverse, unstandardized user-generated content (images and text) to evaluate the CLIP and TF-IDF models.

🔍**Technical Challenge: React SPA Handling**

Challenge: The target platform (Carousell) is a complex React-based SPA where content is rendered asynchronously.

Solution: 
1. Asynchronous Rendering: Solved the issue of missing elements in the initial DOM by using Selenium Explicit Waits(WebDriverWait), ensuring the script only proceeds when the React components are fully loaded.
2. Dynamic Attribute Handling: Developed adaptive XPath selectors using the starts-with() function to maintain scraper stability against React's dynamic data-testid attribute naming conventions.
3. Infinite Scroll Automation: Use custom JavaScript snippets to trigger the platform's lazy-loading mechanism, enabling the extraction of listings that are only rendered upon scrolling.


<details>
  <summary><b>🚀 Smart AI Matching (Multimodal Fusion)</b></summary>
  <br>

| Component | Technical Implementation |
| :--- | :--- |
| **Textual Semantics** | Implements **TF-IDF Vectorization** and **Cosine Similarity** to perform textual analysis on product titles and descriptions. |
| **Visual Similarity** | Use **OpenAI's CLIP (ViT-B-32)** to extract high-dimensional image embeddings, enabling visual recognition beyond simple pixel matching. |
| **Automated Data Pipeline** | Fully containerized using **Docker**, ensuring environment consistency for both the crawler and AI inference engine. |
| **Heuristic Matching Logic** | A **two-stage verification** process that cross-references visual and textual scores to minimize False Positives. |

</details>

<details>
  <summary><b>🔍 Analysis Layers (Step-by-Step)</b></summary>
  <br>

| Stage | Process Description |
| :--- | :--- |
| **Stage 1 (Text-Based)** | Initial screening using textual features to identify high-probability candidate pairs. |
| **Stage 2 (Vision-Based)** | Visual comparison using **CLIP embeddings** to finalize item identification. |

</details>

<details>
  <summary><b>🛠️ Tech Stack</b></summary>
  <br>

| Category | Technologies & Tools |
| :--- | :--- |
| **Core** | Python 3.10 (Slim-buster) |
| **AI / ML** | PyTorch, OpenCLIP, Scikit-learn |
| **Database** | MySQL 8.0, phpMyAdmin |
| **Infrastructure** | Docker, Docker-Compose |
| **Automation** | Selenium, Undetected-ChromeDriver |

</details>

🛠️ **Maintenance & Contributions**

**Web Structure Change**: Since the target platform (Carousell) frequently updates its web architecture, certain selectors may become deprecated over time.

**Found a Bug?**: If the crawler fails to extract data due to UI changes, please feel free to Open an Issue or contact me directly.

**Want to Contribute?**: Contributions are highly welcome! If you've updated the XPath selectors or improved the AI pipeline, please submit a Pull Request. Thanks!

🚀 **Getting Started**
1. Clone the Repository
2. Create a .env file in the root directory (refer to .env.example)
3. docker-compose up --build -d
4. docker-compose logs -f carousell-crawler  //General command to view logs for the crawler service
5. Database: Open http://localhost:8080 to access phpMyAdmin. Use root as the username and your defined password to view results


⚖️ **Disclaimer**

Educational Purpose: This project is strictly for educational and research purposes.

Academic Integrity: Developed to explore the implementation of multimodal AI in real-world data scenarios.

No Data Redistribution: This repository does not contain any scraped datasets or copyrighted imagery.

Legal Compliance: The author is not responsible for any misuse of this tool. Users must comply with the target website's Terms of Service and local regulations.


📜 **License**

This project is licensed under the MIT License.



