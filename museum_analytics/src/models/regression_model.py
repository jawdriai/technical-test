"""
Linear regression model for museum visitor and city population correlation.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, Optional
import logging
import joblib
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MuseumRegressionModel:
    """Linear regression model for museum visitor and city population correlation."""
    
    def __init__(self, model_path: str = "museum_regression_model.pkl"):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.model_path = model_path
        self.is_trained = False
        self.feature_columns = ['city_population']
        self.target_column = 'annual_visitors'
    
    def load_data(self, data_file: str) -> pd.DataFrame:
        """Load harmonized data for training."""
        try:
            df = pd.read_csv(data_file)
            logger.info(f"Loaded {len(df)} records from {data_file}")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def prepare_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare data for training by removing missing values and outliers."""
        if df.empty:
            logger.error("Empty dataframe provided")
            return pd.DataFrame(), pd.Series()
        
        # Remove rows with missing population data
        df_clean = df.dropna(subset=['city_population', 'annual_visitors'])
        logger.info(f"Removed {len(df) - len(df_clean)} rows with missing data")
        
        # Remove outliers using IQR method
        Q1 = df_clean['annual_visitors'].quantile(0.25)
        Q3 = df_clean['annual_visitors'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df_clean = df_clean[
            (df_clean['annual_visitors'] >= lower_bound) & 
            (df_clean['annual_visitors'] <= upper_bound)
        ]
        logger.info(f"Removed outliers, {len(df_clean)} records remaining")
        
        # Prepare features and target
        X = df_clean[self.feature_columns]
        y = df_clean[self.target_column]
        
        return X, y
    
    def train(self, data_file: str, test_size: float = 0.2, random_state: int = 42) -> Dict:
        """Train the linear regression model."""
        logger.info("Starting model training")
        
        # Load and prepare data
        df = self.load_data(data_file)
        if df.empty:
            return {'error': 'Failed to load data'}
        
        X, y = self.prepare_data(df)
        if X.empty or y.empty:
            return {'error': 'Failed to prepare data'}
        
        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        # Make predictions
        y_train_pred = self.model.predict(X_train_scaled)
        y_test_pred = self.model.predict(X_test_scaled)
        
        # Calculate metrics
        train_mse = mean_squared_error(y_train, y_train_pred)
        test_mse = mean_squared_error(y_test, y_test_pred)
        train_r2 = r2_score(y_train, y_train_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        train_mae = mean_absolute_error(y_train, y_train_pred)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        
        # Calculate correlation coefficient
        correlation = np.corrcoef(X_train['city_population'], y_train)[0, 1]
        
        metrics = {
            'train_mse': train_mse,
            'test_mse': test_mse,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'train_mae': train_mae,
            'test_mae': test_mae,
            'correlation': correlation,
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'coefficients': self.model.coef_.tolist(),
            'intercept': self.model.intercept_
        }
        
        logger.info(f"Model training completed. Test R²: {test_r2:.4f}, Correlation: {correlation:.4f}")
        
        # Save model
        self.save_model()
        
        return metrics
    
    def predict(self, city_population: float) -> float:
        """Make prediction for a given city population."""
        if not self.is_trained:
            logger.error("Model not trained yet")
            return 0.0
        
        # Prepare input data
        X = np.array([[city_population]])
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        prediction = self.model.predict(X_scaled)[0]
        return prediction
    
    def save_model(self):
        """Save the trained model and scaler."""
        if not self.is_trained:
            logger.warning("Model not trained, cannot save")
            return
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column
        }
        
        joblib.dump(model_data, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load a previously trained model."""
        try:
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_columns = model_data['feature_columns']
            self.target_column = model_data['target_column']
            self.is_trained = True
            logger.info(f"Model loaded from {self.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
    
    def create_visualizations(self, data_file: str, output_dir: str = "plots"):
        """Create visualization plots for the model."""
        if not self.is_trained:
            logger.error("Model not trained yet")
            return
        
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Load data
        df = self.load_data(data_file)
        if df.empty:
            return
        
        X, y = self.prepare_data(df)
        if X.empty or y.empty:
            return
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        y_pred = self.model.predict(X_scaled)
        
        # Set style
        plt.style.use('seaborn-v0_8')
        
        # 1. Scatter plot with regression line
        plt.figure(figsize=(12, 8))
        plt.scatter(X['city_population'], y, alpha=0.6, color='blue', label='Actual')
        plt.scatter(X['city_population'], y_pred, alpha=0.6, color='red', label='Predicted')
        
        # Sort for smooth line
        sorted_indices = np.argsort(X['city_population'])
        plt.plot(X['city_population'].iloc[sorted_indices], 
                y_pred[sorted_indices], 'r-', linewidth=2, label='Regression Line')
        
        plt.xlabel('City Population')
        plt.ylabel('Annual Visitors')
        plt.title('Museum Visitors vs City Population')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/regression_plot.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Residual plot
        residuals = y - y_pred
        plt.figure(figsize=(10, 6))
        plt.scatter(y_pred, residuals, alpha=0.6)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/residual_plot.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Distribution of residuals
        plt.figure(figsize=(10, 6))
        plt.hist(residuals, bins=20, alpha=0.7, edgecolor='black')
        plt.xlabel('Residuals')
        plt.ylabel('Frequency')
        plt.title('Distribution of Residuals')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/residual_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Q-Q plot for normality check
        from scipy import stats
        plt.figure(figsize=(10, 6))
        stats.probplot(residuals, dist="norm", plot=plt)
        plt.title('Q-Q Plot of Residuals')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/qq_plot.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualizations saved to {output_dir}/")
    
    def get_model_summary(self) -> Dict:
        """Get model summary information."""
        if not self.is_trained:
            return {'error': 'Model not trained'}
        
        summary = {
            'model_type': 'Linear Regression',
            'feature': 'city_population',
            'target': 'annual_visitors',
            'coefficient': self.model.coef_[0],
            'intercept': self.model.intercept_,
            'equation': f"visitors = {self.model.coef_[0]:.2f} * population + {self.model.intercept_:.2f}"
        }
        
        return summary


def main():
    """Main function to run the model training."""
    model = MuseumRegressionModel()
    
    # Check if harmonized data exists
    data_file = "harmonized_museum_data.csv"
    if not Path(data_file).exists():
        print("Please run the data harmonization script first to generate input data")
        return
    
    # Train model
    metrics = model.train(data_file)
    
    if 'error' in metrics:
        print(f"Error: {metrics['error']}")
        return
    
    print("Model Training Results:")
    print(f"Training R²: {metrics['train_r2']:.4f}")
    print(f"Test R²: {metrics['test_r2']:.4f}")
    print(f"Correlation: {metrics['correlation']:.4f}")
    print(f"Training MSE: {metrics['train_mse']:,.2f}")
    print(f"Test MSE: {metrics['test_mse']:,.2f}")
    print(f"Training MAE: {metrics['train_mae']:,.2f}")
    print(f"Test MAE: {metrics['test_mae']:,.2f}")
    
    # Get model summary
    summary = model.get_model_summary()
    print(f"\nModel Equation: {summary['equation']}")
    
    # Create visualizations
    model.create_visualizations(data_file)
    print("\nVisualizations created in 'plots/' directory")
    
    # Test prediction
    test_population = 5_000_000
    prediction = model.predict(test_population)
    print(f"\nPrediction for city with {test_population:,} population: {prediction:,.0f} visitors")


if __name__ == "__main__":
    main()