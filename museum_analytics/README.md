# Museum Analytics Package

This package provides a comprehensive solution for analyzing museum visitor data and its correlation with city population. It includes data extraction, processing, machine learning, and visualization components.

## 📦 Package Structure

```
museum_analytics/
├── __init__.py
├── src/
│   ├── data_extraction/     # Data collection modules
│   ├── data_processing/     # Data harmonization
│   ├── models/             # Machine learning
│   └── database/           # Database operations
├── notebooks/              # Jupyter notebooks
└── README.md              # This file
```

## 🔧 Modules

### Data Extraction (`src/data_extraction/`)

#### `wikipedia_scraper.py`
Extracts museum data from Wikipedia's "List of most visited museums" page.

**Key Features:**
- Robust web scraping with BeautifulSoup
- Handles multiple data formats and table structures
- Extracts visitor numbers with various formats (millions, billions, raw numbers)
- Fallback parsing for different page layouts
- Comprehensive error handling and logging

**Usage:**
```python
from museum_analytics.src.data_extraction.wikipedia_scraper import WikipediaMuseumScraper

scraper = WikipediaMuseumScraper()
museums = scraper.extract_museum_data()
```

#### `population_data.py`
Extracts city population data from multiple sources.

**Key Features:**
- REST Countries API integration
- Manual city-specific data for major metropolitan areas
- Comprehensive city-country mapping
- Fallback mechanisms for missing data
- Support for 500+ cities worldwide

**Usage:**
```python
from museum_analytics.src.data_extraction.population_data import PopulationDataExtractor

extractor = PopulationDataExtractor()
population_data = extractor.get_city_population_data(['Paris', 'London', 'Tokyo'])
```

### Data Processing (`src/data_processing/`)

#### `harmonizer.py`
Harmonizes museum and population data into a unified dataset.

**Key Features:**
- Fuzzy matching of city names
- Data normalization and cleaning
- SQLite database integration
- Visitor-population ratio calculation
- Comprehensive data validation

**Usage:**
```python
from museum_analytics.src.data_processing.harmonizer import DataHarmonizer

harmonizer = DataHarmonizer("museum_analytics.db")
harmonized_df = harmonizer.harmonize_data("museum_data.csv", "city_population.csv")
```

### Machine Learning (`src/models/`)

#### `regression_model.py`
Linear regression model for museum visitor prediction.

**Key Features:**
- Log transformation for better fit with count data
- StandardScaler for feature normalization
- Comprehensive model evaluation metrics
- Visualization generation
- Model persistence with joblib

**Usage:**
```python
from museum_analytics.src.models.regression_model import MuseumRegressionModel

model = MuseumRegressionModel()
metrics = model.train("harmonized_museum_data.csv")
prediction = model.predict(5_000_000)
```

### Database (`src/database/`)

#### `db_manager.py`
Database operations and query management.

**Key Features:**
- SQLite database management
- Complex query support
- Data export capabilities
- Database backup functionality
- Comprehensive statistics

**Usage:**
```python
from museum_analytics.src.database.db_manager import DatabaseManager

db = DatabaseManager("museum_analytics.db")
top_museums = db.get_top_museums(10)
stats = db.get_correlation_stats()
```

## 📊 Data Flow

1. **Extraction**: Museum data from Wikipedia + Population data from APIs
2. **Harmonization**: Match cities and create unified dataset
3. **Storage**: Save to SQLite database and CSV files
4. **Modeling**: Train linear regression model
5. **Analysis**: Generate insights and visualizations

## 🎯 Key Features

- **Modular Design**: Each component can be used independently
- **Robust Error Handling**: Comprehensive logging and graceful failures
- **Data Validation**: Quality checks throughout the pipeline
- **Scalable Architecture**: Easy to extend with new features
- **Docker Support**: Containerized deployment
- **Interactive Analysis**: Jupyter notebook integration

## 📈 Model Performance

The linear regression model typically achieves:
- **R² Score**: 0.3-0.7 (depending on data quality)
- **Correlation**: 0.5-0.8 between city population and museum visitors
- **Log Transformation**: Improves model fit for count data
- **Cross-validation**: Robust performance evaluation

## 🔍 Usage Patterns

### Complete Pipeline
```python
# Run the entire pipeline
python run_pipeline.py
```

### Individual Components
```python
# Extract museum data
python -m museum_analytics.src.data_extraction.wikipedia_scraper

# Extract population data
python -m museum_analytics.src.data_extraction.population_data

# Harmonize data
python -m museum_analytics.src.data_processing.harmonizer

# Train model
python -m museum_analytics.src.models.regression_model
```

### Programmatic Usage
```python
from museum_analytics.src.data_extraction.wikipedia_scraper import WikipediaMuseumScraper
from museum_analytics.src.data_extraction.population_data import PopulationDataExtractor
from museum_analytics.src.data_processing.harmonizer import DataHarmonizer
from museum_analytics.src.models.regression_model import MuseumRegressionModel

# Complete workflow
scraper = WikipediaMuseumScraper()
museums = scraper.extract_museum_data()

extractor = PopulationDataExtractor()
cities = [museum['city'] for museum in museums]
population_data = extractor.get_city_population_data(cities)

harmonizer = DataHarmonizer()
harmonized_df = harmonizer.harmonize_data("museum_data.csv", "city_population.csv")

model = MuseumRegressionModel()
metrics = model.train("harmonized_museum_data.csv")
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the package is installed with `pip install -e .`
2. **Missing Dependencies**: Install all requirements with `pip install -r requirements.txt`
3. **Data Extraction Failures**: Check internet connection and Wikipedia API status
4. **Database Errors**: Ensure SQLite database permissions and disk space

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Dependencies

- pandas >= 2.2
- numpy >= 2.0
- scikit-learn >= 1.5.2
- matplotlib >= 3.9.0
- seaborn == 0.13.0
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.2
- jupyter >= 1.0.0
- lxml >= 5.3.0

## 🚀 Future Enhancements

- Additional data sources (tourism, economic indicators)
- Advanced ML models (ensemble methods, deep learning)
- Real-time data updates
- Web API interface
- Geographic visualization
- Multi-language support

---

*This package provides a complete solution for museum analytics, from data extraction to machine learning model deployment.*