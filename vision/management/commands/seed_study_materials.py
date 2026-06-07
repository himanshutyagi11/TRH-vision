"""
Management command: seed_study_materials
Run with: python manage.py seed_study_materials

Seeds professional learning material content for all Data Analytics tasks.
Safe to run multiple times – it will update existing materials, not duplicate them.
"""
from django.core.management.base import BaseCommand
from vision.models import Task, LearningMaterial


MATERIALS = {
    # ─────────────────────────────────────────────────────────────────────────
    # Match by task title keywords. Keys are lowercase substrings of task titles.
    # Each entry has a list of weeks, each week has a list of materials.
    # ─────────────────────────────────────────────────────────────────────────

    "foundations of data engineering": [
        {
            "week": 1,
            "items": [
                {
                    "title": "What is Data Engineering?",
                    "order": 1,
                    "content": """
<h3>📌 Introduction to Data Engineering</h3>
<p>Data Engineering is the practice of <strong>collecting, transforming, and delivering data</strong> reliably so that analysts and data scientists can use it effectively.</p>

<h4>🔑 Core Responsibilities</h4>
<ul>
  <li>Build and maintain <strong>data pipelines</strong> (ETL/ELT)</li>
  <li>Design and manage <strong>data warehouses</strong> and <strong>data lakes</strong></li>
  <li>Ensure <strong>data quality, reliability, and availability</strong></li>
  <li>Collaborate with analysts and data scientists</li>
</ul>

<h4>📊 Data Engineering vs Data Science</h4>
<table class="table table-bordered table-sm mt-2">
  <thead class="table-dark"><tr><th>Data Engineer</th><th>Data Scientist</th></tr></thead>
  <tbody>
    <tr><td>Builds pipelines</td><td>Uses data for models</td></tr>
    <tr><td>Focuses on infrastructure</td><td>Focuses on insights</td></tr>
    <tr><td>SQL, Python, Spark</td><td>Python, R, ML libraries</td></tr>
  </tbody>
</table>

<blockquote class="blockquote border-start border-4 border-primary ps-3 text-muted">
  <em>"Data engineers are the plumbers of the data world — they make sure the water flows cleanly before anyone can drink it."</em>
</blockquote>
""",
                },
                {
                    "title": "The Data Pipeline: A to Z",
                    "order": 2,
                    "content": """
<h3>🔁 What is a Data Pipeline?</h3>
<p>A data pipeline automates the flow of data from <strong>source → transformation → destination</strong>.</p>

<h4>Pipeline Stages</h4>
<ol>
  <li><strong>Ingestion</strong> – Pull data from APIs, databases, files (CSV, JSON)</li>
  <li><strong>Storage</strong> – Raw data lands in a data lake (e.g., AWS S3, Azure Blob)</li>
  <li><strong>Processing</strong> – Clean, transform, enrich the data</li>
  <li><strong>Serving</strong> – Load into a warehouse (Snowflake, BigQuery, Redshift)</li>
  <li><strong>Visualization</strong> – Business users query via Power BI, Tableau, etc.</li>
</ol>

<h4>🛠 Common Pipeline Tools</h4>
<ul>
  <li><strong>Orchestration:</strong> Apache Airflow, Prefect, Azure Data Factory</li>
  <li><strong>Processing:</strong> Apache Spark, dbt, Pandas</li>
  <li><strong>Storage:</strong> AWS S3, Azure Data Lake</li>
  <li><strong>Warehousing:</strong> Snowflake, BigQuery, Redshift</li>
</ul>

<div class="alert alert-info mt-3">
  <strong>💡 Key Insight:</strong> A pipeline is only as reliable as its weakest component. Always build with error handling and monitoring in mind.
</div>
""",
                },
            ],
        },
        {
            "week": 2,
            "items": [
                {
                    "title": "Data Visualization Fundamentals",
                    "order": 1,
                    "content": """
<h3>📊 The Art of Data Visualization</h3>
<p>Visualization turns raw numbers into <strong>actionable stories</strong>. The right chart type is critical.</p>

<h4>Chart Selection Guide</h4>
<table class="table table-bordered table-sm">
  <thead class="table-dark">
    <tr><th>Goal</th><th>Chart Type</th><th>Example Use</th></tr>
  </thead>
  <tbody>
    <tr><td>Compare values</td><td>Bar / Column Chart</td><td>Sales by region</td></tr>
    <tr><td>Show trend over time</td><td>Line Chart</td><td>Monthly revenue</td></tr>
    <tr><td>Show proportions</td><td>Pie / Donut Chart</td><td>Market share</td></tr>
    <tr><td>Show distribution</td><td>Histogram</td><td>Age distribution</td></tr>
    <tr><td>Show correlation</td><td>Scatter Plot</td><td>Price vs demand</td></tr>
    <tr><td>Show KPIs</td><td>Card / Gauge</td><td>Total sales today</td></tr>
  </tbody>
</table>

<h4>✅ Best Practices</h4>
<ul>
  <li>Less is more – remove chart junk (gridlines, borders, 3D effects)</li>
  <li>Use <strong>colour with purpose</strong> — highlight the key insight</li>
  <li>Label axes clearly with units</li>
  <li>Start bar charts at zero</li>
</ul>

<div class="alert alert-success mt-3">
  <strong>🎯 Rule of Thumb:</strong> A great chart answers ONE question clearly. If you need to explain it, redesign it.
</div>
""",
                },
                {
                    "title": "Excel for Data Analysis — Quick Mastery",
                    "order": 2,
                    "content": """
<h3>📗 Excel as a Data Tool</h3>
<p>Excel remains the most widely used data tool in business. Mastering it is non-negotiable for a data analyst.</p>

<h4>🔑 Must-Know Functions</h4>
<ul>
  <li><code>VLOOKUP / XLOOKUP</code> – Match records across tables</li>
  <li><code>IF / IFS / SWITCH</code> – Conditional logic</li>
  <li><code>SUMIF / COUNTIF / AVERAGEIF</code> – Aggregate with conditions</li>
  <li><code>INDEX + MATCH</code> – More flexible than VLOOKUP</li>
  <li><code>TEXT / LEFT / RIGHT / MID</code> – String manipulation</li>
  <li><code>PIVOT TABLES</code> – Summarise thousands of rows instantly</li>
</ul>

<h4>⚡ Power Features</h4>
<ul>
  <li><strong>Power Query (Get & Transform)</strong> – Import and clean data from multiple sources</li>
  <li><strong>Power Pivot</strong> – Build data models with relationships and DAX measures</li>
  <li><strong>Sparklines</strong> – Mini in-cell charts</li>
  <li><strong>Conditional Formatting</strong> – Visual heatmaps and data bars</li>
</ul>
""",
                },
            ],
        },
        {
            "week": 3,
            "items": [
                {
                    "title": "Introduction to SQL for Analytics",
                    "order": 1,
                    "content": """
<h3>🗃 SQL — The Language of Data</h3>
<p>SQL (Structured Query Language) is the primary tool for querying relational databases. Every data analyst <strong>must</strong> know SQL.</p>

<h4>SQL Query Structure</h4>
<pre><code class="language-sql">SELECT   column1, column2, COUNT(*) AS total
FROM     table_name
WHERE    condition = 'value'
GROUP BY column1, column2
HAVING   COUNT(*) > 5
ORDER BY total DESC
LIMIT    10;</code></pre>

<h4>📋 Core Clauses</h4>
<table class="table table-sm table-bordered">
  <thead class="table-dark"><tr><th>Clause</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr><td><code>SELECT</code></td><td>Choose which columns to return</td></tr>
    <tr><td><code>FROM</code></td><td>Which table to query</td></tr>
    <tr><td><code>WHERE</code></td><td>Filter rows before aggregation</td></tr>
    <tr><td><code>GROUP BY</code></td><td>Aggregate rows into groups</td></tr>
    <tr><td><code>HAVING</code></td><td>Filter groups after aggregation</td></tr>
    <tr><td><code>ORDER BY</code></td><td>Sort results</td></tr>
  </tbody>
</table>

<h4>🔗 JOIN Types</h4>
<ul>
  <li><strong>INNER JOIN</strong> – Only matching rows from both tables</li>
  <li><strong>LEFT JOIN</strong> – All from left + matching from right (NULL if no match)</li>
  <li><strong>RIGHT JOIN</strong> – All from right + matching from left</li>
  <li><strong>FULL OUTER JOIN</strong> – All rows from both tables</li>
</ul>
""",
                },
            ],
        },
        {
            "week": 4,
            "items": [
                {
                    "title": "Capstone Review & Best Practices",
                    "order": 1,
                    "content": """
<h3>🏆 Week 4 — Bringing It All Together</h3>
<p>This week we consolidate everything learned in the module and apply best practices used in professional data engineering teams.</p>

<h4>✅ Data Engineering Checklist</h4>
<ul>
  <li>☑ Understand the business question before building anything</li>
  <li>☑ Document your data sources and transformations</li>
  <li>☑ Validate data quality at each pipeline step</li>
  <li>☑ Build idempotent pipelines (safe to re-run)</li>
  <li>☑ Monitor for failures with alerts</li>
  <li>☑ Version control your code (Git)</li>
</ul>

<h4>📌 Industry Tools Summary</h4>
<table class="table table-sm table-bordered">
  <thead class="table-dark"><tr><th>Category</th><th>Tools</th></tr></thead>
  <tbody>
    <tr><td>Ingestion</td><td>Fivetran, Airbyte, Kafka</td></tr>
    <tr><td>Transformation</td><td>dbt, Spark, Pandas</td></tr>
    <tr><td>Orchestration</td><td>Airflow, Prefect, Dagster</td></tr>
    <tr><td>Warehouse</td><td>Snowflake, BigQuery, Redshift</td></tr>
    <tr><td>Visualisation</td><td>Power BI, Looker, Tableau</td></tr>
  </tbody>
</table>

<div class="alert alert-warning">
  <strong>📝 Assignment:</strong> Write a 1-page data flow diagram for a fictional e-commerce business. Identify: data sources, transformations needed, and dashboard KPIs.
</div>
""",
                },
            ],
        },
    ],

    # ─────────────────────────────────────────────────────────────────────────
    "power query": [
        {
            "week": 1,
            "items": [
                {
                    "title": "Power Query — The ETL Engine in Excel & Power BI",
                    "order": 1,
                    "content": """
<h3>⚡ What is Power Query?</h3>
<p>Power Query (also called <strong>Get & Transform</strong>) is Microsoft's built-in ETL tool in Excel and Power BI. It lets you <strong>connect, clean, and shape data</strong> without writing a single line of code.</p>

<h4>🔗 Data Sources You Can Connect To</h4>
<ul>
  <li>Excel (.xlsx, .csv) files</li>
  <li>SQL Server, MySQL, PostgreSQL databases</li>
  <li>SharePoint, OneDrive</li>
  <li>Web pages (HTML tables)</li>
  <li>REST APIs (JSON / XML)</li>
  <li>Azure, AWS, Google Sheets</li>
</ul>

<h4>🔁 The ETL Process in Power Query</h4>
<ol>
  <li><strong>Extract</strong> – Connect to a data source</li>
  <li><strong>Transform</strong> – Clean, filter, split, merge columns</li>
  <li><strong>Load</strong> – Push clean data into the data model</li>
</ol>

<div class="alert alert-info">
  <strong>💡 Why Power Query?</strong> Every transformation step is recorded and <strong>auto-replays when data refreshes</strong>. No manual re-cleaning every day!
</div>
""",
                },
                {
                    "title": "Common Transformations in Power Query",
                    "order": 2,
                    "content": """
<h3>🛠 Essential Power Query Transformations</h3>

<h4>1. Remove / Keep Rows</h4>
<p>Filter out blank rows, errors, or rows that don't match your criteria.</p>

<h4>2. Split Column</h4>
<p>Split <code>FirstName LastName</code> into two separate columns by delimiter (space, comma, etc.)</p>

<h4>3. Merge Columns</h4>
<p>Combine <code>City</code> + <code>Country</code> into <code>City, Country</code>.</p>

<h4>4. Change Data Types</h4>
<p>Ensure dates are <strong>Date</strong> type, numbers are <strong>Decimal/Integer</strong>, not text.</p>

<h4>5. Pivot / Unpivot</h4>
<p>Restructure data from wide format (months as columns) to tall format (one row per month) — essential for Power BI.</p>

<h4>6. Merge Queries (JOIN)</h4>
<p>Combine two tables on a matching key — equivalent to SQL <code>JOIN</code>.</p>

<h4>7. Append Queries (UNION)</h4>
<p>Stack two tables with the same columns — equivalent to SQL <code>UNION ALL</code>.</p>

<div class="alert alert-success mt-3">
  <strong>✅ Pro Tip:</strong> Always rename your steps in the Query Settings panel. It makes debugging much easier later.
</div>
""",
                },
            ],
        },
        {
            "week": 2,
            "items": [
                {
                    "title": "M Language Basics",
                    "order": 1,
                    "content": """
<h3>🔤 What is M Language?</h3>
<p>Every Power Query transformation is stored as <strong>M code</strong> behind the scenes. Understanding M lets you write custom logic beyond the GUI.</p>

<h4>Basic M Structure</h4>
<pre><code>let
    Source = Excel.Workbook(File.Contents("data.xlsx"), null, true),
    Sheet1 = Source{[Name="Sales"]}[Data],
    FilteredRows = Table.SelectRows(Sheet1, each [Amount] > 1000),
    RenamedCols = Table.RenameColumns(FilteredRows, {{"Amount", "Revenue"}})
in
    RenamedCols</code></pre>

<h4>Key Concepts</h4>
<ul>
  <li><code>let ... in</code> – The basic M expression block</li>
  <li>Each step creates a new named result</li>
  <li><code>each</code> – Shorthand for a row-level function</li>
  <li>Functions follow pattern: <code>Table.FunctionName(args)</code></li>
</ul>

<div class="alert alert-info">
  <strong>💡 Tip:</strong> Open the Advanced Editor in Power Query to see and edit M code directly.
</div>
""",
                },
            ],
        },
        {
            "week": 3,
            "items": [
                {
                    "title": "Building a Full ETL Pipeline in Power Query",
                    "order": 1,
                    "content": """
<h3>🏗 Building a Real ETL Pipeline</h3>
<p>In this session we put it all together: import raw sales data, clean it, and load a clean model into Power BI.</p>

<h4>📋 Step-by-Step Walkthrough</h4>
<ol>
  <li><strong>Connect</strong> to raw CSV exported from the sales system</li>
  <li><strong>Promote Headers</strong> – First row becomes column names</li>
  <li><strong>Fix Data Types</strong> – Date columns must be Date, amounts must be Number</li>
  <li><strong>Remove Nulls</strong> – Remove rows where CustomerID is blank</li>
  <li><strong>Add Custom Column</strong> – <code>Profit = Revenue - Cost</code></li>
  <li><strong>Merge with Customers table</strong> – Add customer name and region</li>
  <li><strong>Group By Region</strong> – Summarise total revenue by region</li>
  <li><strong>Load to Power BI Report</strong></li>
</ol>

<div class="alert alert-warning">
  <strong>📝 Practice Task:</strong> Download the sample sales CSV and replicate these 8 steps in Power Query. Check your final row count matches the expected 1,247 records.
</div>
""",
                },
            ],
        },
    ],

    # ─────────────────────────────────────────────────────────────────────────
    "data modeling": [
        {
            "week": 1,
            "items": [
                {
                    "title": "What is Data Modeling?",
                    "order": 1,
                    "content": """
<h3>🗂 Data Modeling — The Blueprint of Your Data</h3>
<p>Data modeling is the process of <strong>defining how data is structured, stored, and related</strong>. A good data model makes queries fast, reports accurate, and maintenance easy.</p>

<h4>Types of Data Models</h4>
<ul>
  <li><strong>Conceptual</strong> – High-level entities and relationships (e.g., Customer buys Product)</li>
  <li><strong>Logical</strong> – Detailed attributes and keys, database-agnostic</li>
  <li><strong>Physical</strong> – Actual SQL tables, columns, indexes, as implemented</li>
</ul>

<h4>🔑 Key Terms</h4>
<table class="table table-sm table-bordered">
  <thead class="table-dark"><tr><th>Term</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td>Entity</td><td>A real-world object (Customer, Product, Order)</td></tr>
    <tr><td>Attribute</td><td>A property of an entity (Name, Price, Date)</td></tr>
    <tr><td>Primary Key (PK)</td><td>Unique identifier for each row</td></tr>
    <tr><td>Foreign Key (FK)</td><td>A PK from another table, creating the relationship</td></tr>
    <tr><td>Relationship</td><td>How entities relate (one-to-many, many-to-many)</td></tr>
  </tbody>
</table>
""",
                },
                {
                    "title": "The Star Schema — Power BI's Best Friend",
                    "order": 2,
                    "content": """
<h3>⭐ Star Schema</h3>
<p>The star schema is the <strong>most popular model for analytical databases and Power BI</strong>. It separates data into <strong>Fact tables</strong> and <strong>Dimension tables</strong>.</p>

<h4>Structure</h4>
<ul>
  <li><strong>Fact Table</strong> – Central table storing measurable events (Sales, Orders, Clicks). Contains numeric measures and FK references.</li>
  <li><strong>Dimension Tables</strong> – Descriptive context (Date, Customer, Product, Geography). Contain text attributes and PK.</li>
</ul>

<h4>Example: Sales Star Schema</h4>
<pre><code>FactSales
  ├── SaleID (PK)
  ├── DateKey (FK → DimDate)
  ├── CustomerKey (FK → DimCustomer)
  ├── ProductKey (FK → DimProduct)
  ├── Revenue
  └── Quantity

DimDate: DateKey, Date, Month, Quarter, Year
DimCustomer: CustomerKey, Name, City, Segment
DimProduct: ProductKey, ProductName, Category, SubCategory</code></pre>

<h4>✅ Why Star Schema?</h4>
<ul>
  <li>Simple to understand for business users</li>
  <li>Fast query performance (fewer JOINs)</li>
  <li>Works perfectly with Power BI relationships</li>
  <li>Easier to add new dimensions later</li>
</ul>
""",
                },
            ],
        },
        {
            "week": 2,
            "items": [
                {
                    "title": "Relationships in Power BI",
                    "order": 1,
                    "content": """
<h3>🔗 Relationships in Power BI Data Model</h3>
<p>Relationships allow Power BI to filter data across tables automatically — the core of the data model.</p>

<h4>Types of Cardinality</h4>
<ul>
  <li><strong>One-to-Many (1:*)</strong> – Most common. One product can appear in many sales. Dimension → Fact.</li>
  <li><strong>One-to-One (1:1)</strong> – Rare. Usually means tables can be merged.</li>
  <li><strong>Many-to-Many (*:*)</strong> – Use carefully. Requires a bridge table for best results.</li>
</ul>

<h4>Cross Filter Direction</h4>
<ul>
  <li><strong>Single</strong> (default) – Filter flows from the 1 side to the many side</li>
  <li><strong>Both</strong> – Filters flow in both directions (use with care — can cause ambiguity)</li>
</ul>

<div class="alert alert-danger">
  <strong>⚠ Common Mistake:</strong> Using Many-to-Many relationships when a proper Star Schema with a bridge table would work better. Always prefer 1:* where possible.
</div>

<h4>Active vs Inactive Relationships</h4>
<p>Only one relationship between two tables can be <strong>active</strong> at a time. Use <code>USERELATIONSHIP()</code> in DAX to activate an inactive relationship in a specific measure.</p>
""",
                },
            ],
        },
        {
            "week": 3,
            "items": [
                {
                    "title": "DAX Measures — Calculations That Power Reports",
                    "order": 1,
                    "content": """
<h3>📐 DAX — Data Analysis Expressions</h3>
<p>DAX is the formula language of Power BI (and Power Pivot). It is used to create <strong>calculated columns</strong> and <strong>measures</strong>.</p>

<h4>Measure vs Calculated Column</h4>
<table class="table table-sm table-bordered">
  <thead class="table-dark"><tr><th></th><th>Measure</th><th>Calculated Column</th></tr></thead>
  <tbody>
    <tr><td>When calculated</td><td>At query time (dynamic)</td><td>At refresh time (static)</td></tr>
    <tr><td>Context aware</td><td>✅ Yes</td><td>❌ Row context only</td></tr>
    <tr><td>Best for</td><td>KPIs, aggregations</td><td>Row-level attributes</td></tr>
  </tbody>
</table>

<h4>Essential DAX Measures</h4>
<pre><code>-- Basic aggregations
Total Revenue = SUM(FactSales[Revenue])
Total Orders = COUNTROWS(FactSales)
Avg Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

-- Time intelligence
Revenue LY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))
YoY Growth % = DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY], 0)

-- Filtered measure
Revenue - Online = CALCULATE([Total Revenue], DimChannel[Channel] = "Online")</code></pre>

<h4>🔑 Key Functions</h4>
<ul>
  <li><code>CALCULATE()</code> – Modify the filter context (the most powerful DAX function)</li>
  <li><code>FILTER()</code> – Create a filtered table</li>
  <li><code>ALL()</code> – Remove all filters from a table/column</li>
  <li><code>RELATED()</code> – Lookup a value from a related table</li>
  <li><code>DIVIDE()</code> – Safe division (avoids divide-by-zero errors)</li>
</ul>
""",
                },
            ],
        },
    ],

    # ─────────────────────────────────────────────────────────────────────────
    "power bi": [
        {
            "week": 1,
            "items": [
                {
                    "title": "Power BI Desktop — Getting Started",
                    "order": 1,
                    "content": """
<h3>📊 Introduction to Power BI</h3>
<p>Power BI is Microsoft's leading <strong>Business Intelligence platform</strong>. It connects to hundreds of data sources and creates interactive reports and dashboards.</p>

<h4>Power BI Ecosystem</h4>
<ul>
  <li><strong>Power BI Desktop</strong> – Free Windows app to build reports</li>
  <li><strong>Power BI Service</strong> – Web-based publishing, sharing, and collaboration</li>
  <li><strong>Power BI Mobile</strong> – View reports on iOS / Android</li>
  <li><strong>Power BI Gateway</strong> – Refresh on-premises data in the cloud</li>
</ul>

<h4>🔁 The Power BI Workflow</h4>
<ol>
  <li><strong>Get Data</strong> – Connect to your source (Excel, SQL, API)</li>
  <li><strong>Transform</strong> – Clean data with Power Query</li>
  <li><strong>Model</strong> – Define relationships, create measures in DAX</li>
  <li><strong>Report</strong> – Build visuals on the Report canvas</li>
  <li><strong>Publish</strong> – Upload to Power BI Service and share</li>
</ol>

<div class="alert alert-info">
  <strong>💡 Download Power BI Desktop free from:</strong> <a href="https://powerbi.microsoft.com/desktop" target="_blank">powerbi.microsoft.com/desktop</a>
</div>
""",
                },
                {
                    "title": "Building Your First Power BI Report",
                    "order": 2,
                    "content": """
<h3>🛠 Step-by-Step: Your First Report</h3>

<h4>1. Import Data</h4>
<p>Go to <strong>Home → Get Data → Excel</strong>. Select the sample Sales workbook.</p>

<h4>2. Check Data in Power Query</h4>
<p>Fix data types: ensure Date columns are Date, Revenue is Decimal Number.</p>

<h4>3. Create a Simple Measure</h4>
<pre><code>Total Revenue = SUM(Sales[Revenue])</code></pre>

<h4>4. Build Visuals</h4>
<ul>
  <li><strong>Card</strong> – Show Total Revenue</li>
  <li><strong>Bar Chart</strong> – Revenue by Product Category</li>
  <li><strong>Line Chart</strong> – Revenue over Time (Month)</li>
  <li><strong>Slicer</strong> – Filter by Year or Region</li>
  <li><strong>Table</strong> – Top 10 customers by revenue</li>
</ul>

<h4>5. Format Your Report</h4>
<ul>
  <li>Use a consistent colour palette (company brand colours)</li>
  <li>Add a title and subtitle text box</li>
  <li>Align and space visuals neatly</li>
  <li>Remove unnecessary gridlines and borders</li>
</ul>

<h4>6. Publish</h4>
<p>Click <strong>Home → Publish → My Workspace</strong>. View it in your browser at <a href="https://app.powerbi.com" target="_blank">app.powerbi.com</a>.</p>
""",
                },
            ],
        },
        {
            "week": 2,
            "items": [
                {
                    "title": "Advanced Visuals & Interactivity",
                    "order": 1,
                    "content": """
<h3>🎨 Advanced Power BI Visuals</h3>

<h4>Custom Visuals (AppSource)</h4>
<p>Power BI Marketplace offers 300+ custom visuals. Most useful ones:</p>
<ul>
  <li><strong>Hierarchy Slicer</strong> – Filter by Country → City → Store</li>
  <li><strong>Chiclet Slicer</strong> – Button-style slicers</li>
  <li><strong>Enlighten Aquarium</strong> – Animated KPI cards</li>
  <li><strong>Bullet Chart</strong> – Compare actual vs target</li>
</ul>

<h4>Page-Level vs Report-Level Filters</h4>
<table class="table table-sm table-bordered">
  <thead class="table-dark"><tr><th>Filter Scope</th><th>Applies To</th></tr></thead>
  <tbody>
    <tr><td>Visual-level</td><td>Only that one visual</td></tr>
    <tr><td>Page-level</td><td>All visuals on the current page</td></tr>
    <tr><td>Report-level</td><td>All visuals across all pages</td></tr>
  </tbody>
</table>

<h4>Drill-Through</h4>
<p>Right-click on a data point → Drill through to a detail page. Set up by adding fields to the Drill-through bucket on the detail page.</p>

<h4>Bookmarks & Buttons</h4>
<p>Create toggle buttons to switch between chart types or show/hide panels — makes reports feel like proper web apps.</p>
""",
                },
            ],
        },
    ],
}


def find_matching_tasks(keyword):
    """Find tasks whose title contains the keyword (case-insensitive)."""
    return Task.objects.filter(title__icontains=keyword)


class Command(BaseCommand):
    help = "Seed professional study material content into existing Tasks."

    def handle(self, *args, **options):
        total_created = 0
        total_updated = 0

        for keyword, weeks in MATERIALS.items():
            tasks = find_matching_tasks(keyword)
            if not tasks.exists():
                self.stdout.write(
                    self.style.WARNING(f"  [SKIP] No task found matching '{keyword}'")
                )
                continue

            for task in tasks:
                self.stdout.write(f"\n[TASK] {task.title}")

                for week_data in weeks:
                    week_num = week_data["week"]
                    for item in week_data["items"]:
                        obj, created = LearningMaterial.objects.update_or_create(
                            task=task,
                            week_number=week_num,
                            title=item["title"],
                            defaults={
                                "content": item["content"].strip(),
                                "order": item["order"],
                            },
                        )
                        status = "[CREATED]" if created else "[UPDATED]"
                        self.stdout.write(
                            f"  {status} Week {week_num}: {item['title']}"
                        )
                        if created:
                            total_created += 1
                        else:
                            total_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! {total_created} created, {total_updated} updated."
            )
        )
