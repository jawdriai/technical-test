# Museum Analytics: Visitor-Population Correlation Analysis

A comprehensive data engineering solution that analyzes the correlation between museum visitor numbers and city population using linear regression. This project extracts museum data from Wikipedia, combines it with city population data, and builds a machine learning model to understand the relationship.

## 🎯 Project Overview

This project addresses the following requirements:
- Extract museum data from Wikipedia API (museums with >2M annual visitors)
- Integrate city population data from multiple sources
- Build a harmonized database for analysis
- Create a linear regression ML model
- Provide visualizations and insights
- Package everything in Docker containers

## 🏗️ Architecture

```
museum_analytics/
├── src/
│   ├── data_extraction/
│   │   ├── wikipedia_scraper.py    # Wikipedia API scraper
│   │   └── population_data.py      # Population data extractor
│   ├── data_processing/
│   │   └── harmonizer.py           # Data harmonization
│   ├── models/
│   │   └── regression_model.py     # ML model implementation
│   └── database/
│       └── db_manager.py           # Database operations
├── notebooks/
│   └── museum_analysis.ipynb       # Jupyter notebook
├── data/                           # Data storage
├── models/                         # Model storage
├── plots/                          # Visualization outputs
├── Dockerfile                      # Docker configuration
├── docker-compose.yml             # Docker Compose setup
└── run_pipeline.py                # Main execution script
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone and navigate to the project
cd museum-analytics

# Build and run with Docker Compose
docker-compose up --build

# Access Jupyter Lab at http://localhost:8888
```

### Option 2: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .

# Run the complete pipeline
python run_pipeline.py

# Or run individual components
python -m museum_analytics.src.data_extraction.wikipedia_scraper
python -m museum_analytics.src.data_extraction.population_data
python -m museum_analytics.src.data_processing.harmonizer
python -m museum_analytics.src.models.regression_model
```

## 📊 Data Sources

### Museum Data
- **Source**: Wikipedia API
- **Criteria**: Museums with >2,000,000 annual visitors
- **Fields**: Museum name, city, country, annual visitors, year

### Population Data
- **Sources**: 
  - REST Countries API (country-level data)
  - Manual city-specific data for major cities
- **Fields**: City name, country, population

## 🔧 Technical Implementation

### Data Extraction
- **Wikipedia Scraper**: Uses BeautifulSoup to parse museum tables
- **Population Extractor**: Combines API data with manual mappings
- **Error Handling**: Robust error handling and logging

### Data Processing
- **Harmonization**: Matches museum cities with population data
- **Normalization**: Standardizes city names for better matching
- **Database**: SQLite for data storage and querying

### Machine Learning
- **Model**: Linear regression using scikit-learn
- **Features**: City population (independent variable)
- **Target**: Annual museum visitors (dependent variable)
- **Evaluation**: R², MSE, MAE, correlation coefficient

### Visualization
- **Plots**: Scatter plots, residual analysis, Q-Q plots
- **Notebook**: Interactive Jupyter notebook for analysis
- **Output**: High-quality plots saved to files

## 📈 Key Features

1. **Automated Data Pipeline**: End-to-end data extraction and processing
2. **Robust Error Handling**: Comprehensive logging and error management
3. **Scalable Architecture**: Modular design for easy extension
4. **Docker Containerization**: Consistent deployment environment
5. **Interactive Analysis**: Jupyter notebook for exploration
6. **Database Integration**: SQLite for data persistence and querying
7. **Visualization Suite**: Multiple plot types for analysis

## 🎯 Model Performance

The linear regression model provides insights into the relationship between city population and museum attendance:

- **Correlation**: Measures the strength of the relationship
- **R² Score**: Indicates how well the model explains the variance
- **Predictions**: Estimates visitor numbers for different city sizes

## 📋 Requirements

### System Requirements
- Python 3.8+
- Docker (optional)
- 2GB RAM minimum
- 1GB disk space

### Python Dependencies
- pandas >= 2.1.4
- numpy >= 1.24.3
- scikit-learn >= 1.3.2
- matplotlib >= 3.8.2
- seaborn >= 0.13.0
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.2
- jupyter >= 1.0.0

## 🔍 Usage Examples

### Running the Complete Pipeline
```python
from museum_analytics.src.data_extraction.wikipedia_scraper import WikipediaMuseumScraper
from museum_analytics.src.models.regression_model import MuseumRegressionModel

# Extract data
scraper = WikipediaMuseumScraper()
museums = scraper.extract_museum_data()

# Train model
model = MuseumRegressionModel()
metrics = model.train("harmonized_museum_data.csv")

# Make predictions
prediction = model.predict(5_000_000)  # City with 5M population
print(f"Predicted visitors: {prediction:,.0f}")
```

### Database Queries
```python
from museum_analytics.src.database.db_manager import DatabaseManager

db = DatabaseManager("museum_analytics.db")
top_museums = db.get_top_museums(10)
stats = db.get_correlation_stats()
```

## 📊 Output Files

The pipeline generates several output files:

- `data/museum_data.csv`: Raw museum data from Wikipedia
- `data/city_population.csv`: City population data
- `data/harmonized_museum_data.csv`: Combined dataset
- `data/museum_analytics.db`: SQLite database
- `models/museum_regression_model.pkl`: Trained ML model
- `plots/`: Visualization files (PNG format)

## 🎯 Business Insights

The analysis reveals:

1. **Correlation Strength**: How strongly city population correlates with museum attendance
2. **Visitor Ratios**: Average percentage of city population that visits museums
3. **Top Performers**: Museums with highest visitor-population ratios
4. **Predictive Power**: Model accuracy for visitor predictions

## 🔧 Customization

### Adding New Data Sources
1. Extend the `PopulationDataExtractor` class
2. Add new extraction methods
3. Update the harmonization logic

### Modifying the Model
1. Edit `MuseumRegressionModel` class
2. Add new features (tourism, cultural indicators)
3. Try different algorithms (polynomial, random forest)

### Extending Visualizations
1. Add new plot types to the model class
2. Create custom analysis functions
3. Enhance the Jupyter notebook

## 🐛 Troubleshooting

### Common Issues

1. **Wikipedia API Rate Limiting**: The scraper includes delays and error handling
2. **Missing Population Data**: Manual mappings cover major cities
3. **Docker Build Issues**: Ensure Docker has sufficient resources
4. **Import Errors**: Check Python path and package installation

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python run_pipeline.py
```

## 📚 Rationale for Design Choices

### Technology Stack
- **Python**: Excellent for data science and ML
- **SQLite**: Lightweight database for MVP
- **Docker**: Consistent deployment environment
- **Jupyter**: Interactive analysis and visualization

### Architecture Decisions
- **Modular Design**: Easy to extend and maintain
- **Error Handling**: Robust pipeline execution
- **Data Validation**: Quality checks throughout
- **Scalability**: Designed for future enhancements

### Data Sources
- **Wikipedia**: Comprehensive, regularly updated museum data
- **Multiple APIs**: Redundant data sources for reliability
- **Manual Mappings**: Fallback for missing data

## 🚀 Future Enhancements

1. **Additional Features**: Tourism data, cultural indicators
2. **Advanced Models**: Deep learning, ensemble methods
3. **Real-time Updates**: Automated data refresh
4. **Web Interface**: REST API and dashboard
5. **Geographic Analysis**: Spatial clustering and mapping

## 📄 License

This project is created for educational and demonstration purposes.

## 👥 Author

**Jawher** - Data Engineering Assignment

---

*This solution demonstrates a complete data engineering workflow from data extraction to machine learning model deployment, packaged in Docker containers for easy deployment and scaling.*