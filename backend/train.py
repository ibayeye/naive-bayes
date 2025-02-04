import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
import joblib

def load_and_preprocess_data(filepath):
    """Load and preprocess the dataset with additional features"""
    # Load dataset
    df = pd.read_csv(filepath, encoding="ISO-8859-1", delimiter=";")
    
    # Display initial dataset info
    print("Dataset Info:")
    print(df.info())
    print("\nMissing values:")
    print(df.isna().sum())
    
    # Map categorical values
    income_mapping = {"Rendah": 0, "Sedang": 1, "Tinggi": 2}
    distance_mapping = {"Dekat": 0, "Jauh": 1}
    organization_mapping = {"Tidak": 0, "Ikut": 1}
    ukm_mapping = {"Tidak": 0, "Ikut": 1}
    gender_mapping = {"L": 0, "P": 1}
    
    # Apply mappings
    df["Penghasilan"] = df["Penghasilan"].map(income_mapping)
    df["Jarak Tempat Tinggal kekampus (Km)"] = df["Jarak Tempat Tinggal kekampus (Km)"].map(distance_mapping)
    df["Ikut Organisasi"] = df["Ikut Organisasi"].map(organization_mapping)
    df["Ikut UKM"] = df["Ikut UKM"].map(ukm_mapping)
    df["Jenis Kelamin"] = df["Jenis Kelamin"].map(gender_mapping)
    
    # Convert IPK from string to float (assuming IPK is in format like "357" for 3.57)
    df["IPK"] = df["IPK"].astype(float) / 100
    
    # Select relevant features
    selected_features = [
        "IPK",
        "Penghasilan",
        "Tanggungan",
        "Jarak Tempat Tinggal kekampus (Km)",
        "Ikut Organisasi",
        "Ikut UKM",
        "Jenis Kelamin",
        "SKS",
        "Status Beasiswa"
    ]
    
    df = df[selected_features]
    
    # Handle missing values
    numeric_features = ["IPK", "Penghasilan", "Tanggungan", "SKS"]
    imputer = SimpleImputer(strategy="mean")
    df[numeric_features] = imputer.fit_transform(df[numeric_features])
    
    return df

def prepare_features(df):
    """Prepare features and target variables"""
    # Encode target variable
    le = LabelEncoder()
    df["Status Beasiswa"] = le.fit_transform(df["Status Beasiswa"])
    
    # Split features and target
    feature_columns = [
        "IPK",
        "Penghasilan",
        "Tanggungan",
        "Jarak Tempat Tinggal kekampus (Km)",
        "Ikut Organisasi",
        "Ikut UKM",
        "Jenis Kelamin",
        "SKS"
    ]
    
    X = df[feature_columns]
    y = df["Status Beasiswa"]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    
    return X_scaled, y, scaler
def train_and_evaluate_model(X, y, scaler):
    """Train and evaluate model with enhanced features"""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Cek jumlah sampel tiap kelas
    unique, counts = np.unique(y_train, return_counts=True)
    min_samples = min(counts)
    
    # Gunakan SMOTE untuk menyeimbangkan data
    if min_samples >= 6:
        smote = SMOTE(random_state=42)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    else:
        # Jika sampel terlalu sedikit untuk SMOTE, gunakan random oversampling
        from sklearn.utils import resample
        majority_class = 0 if (y_train == 0).sum() > (y_train == 1).sum() else 1
        minority_class = 1 if majority_class == 0 else 0
        
        # Convert to DataFrame untuk memudahkan resampling
        X_train_df = pd.DataFrame(X_train, columns=X.columns)
        train_data = pd.concat([X_train_df, pd.Series(y_train, name='Status')], axis=1)
        
        # Pisahkan mayoritas dan minoritas
        majority_data = train_data[train_data['Status'] == majority_class]
        minority_data = train_data[train_data['Status'] == minority_class]
        
        # Upsample minoritas
        minority_upsampled = resample(minority_data,
                                    replace=True,
                                    n_samples=len(majority_data),
                                    random_state=42)
        
        # Gabungkan kembali
        balanced_data = pd.concat([majority_data, minority_upsampled])
        X_train_balanced = balanced_data.drop('Status', axis=1)
        y_train_balanced = balanced_data['Status']
    
    # Train model
    model = GaussianNB()
    model.fit(X_train_balanced, y_train_balanced)
    
    # Simpan model dan scaler
    joblib.dump(model, "model_naive_bayes_enhanced.pkl")
    joblib.dump(scaler, "scaler_enhanced.pkl")
    print("Model dan scaler berhasil disimpan.")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_balanced, y_train_balanced, cv=5)
    print(f"\nCross-validation scores: {cv_scores.mean():.2f} (+/- {cv_scores.std() * 2:.2f})")
    
    # Predictions dan evaluasi
    y_pred = model.predict(X_test)
    
    # Print metrics
    print(f"\nAccuracy Score: {accuracy_score(y_test, y_pred):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Visualisasi Confusion Matrix
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()
    
    # Feature importance analysis
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': np.abs(model.theta_[1] - model.theta_[0])  # Difference in means between classes
    })
    feature_importance = feature_importance.sort_values('Importance', ascending=False)
    
    # Visualisasi Feature Importance
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=feature_importance)
    plt.title('Feature Importance')
    plt.xlabel('Absolute Difference in Class Means')
    plt.tight_layout()
    plt.show()
    
    return model
def visualize_data(df):
    """Create enhanced visualizations for data analysis"""
    plt.figure(figsize=(15, 10))
    
    # Distribution of Scholarship Status
    plt.subplot(2, 2, 1)
    sns.countplot(x="Status Beasiswa", data=df)
    plt.title("Distribution of Scholarship Status")
    
    # IPK vs Tanggungan
    plt.subplot(2, 2, 2)
    scatter = plt.scatter(df["IPK"], df["Tanggungan"], 
                         c=df["Status Beasiswa"], cmap='viridis')
    plt.colorbar(scatter)
    plt.xlabel("IPK")
    plt.ylabel("Tanggungan")
    plt.title("IPK vs Tanggungan by Scholarship Status")
    
    # Organization and UKM participation
    plt.subplot(2, 2, 3)
    org_ukm_counts = df.groupby(["Ikut Organisasi", "Ikut UKM", "Status Beasiswa"]).size().unstack()
    org_ukm_counts.plot(kind='bar')
    plt.title("Scholarship Status by Organization and UKM Participation")
    plt.xlabel("(Organization, UKM)")
    
    # Income level distribution
    plt.subplot(2, 2, 4)
    sns.boxplot(x="Status Beasiswa", y="Penghasilan", data=df)
    plt.title("Income Distribution by Scholarship Status")
    
    plt.tight_layout()
    plt.show()
    

def predict_new_student(model, scaler, ipk, penghasilan, tanggungan, jarak, organisasi, ukm, gender, sks):
    """Make prediction for a new student with enhanced features"""
    # Prepare input data
    new_data = pd.DataFrame([[ipk, penghasilan, tanggungan, jarak, organisasi, ukm, gender, sks]], 
                           columns=['IPK', 'Penghasilan', 'Tanggungan', 
                                  'Jarak Tempat Tinggal kekampus (Km)',
                                  'Ikut Organisasi', 'Ikut UKM', 
                                  'Jenis Kelamin', 'SKS'])
    new_data_scaled = scaler.transform(new_data)
    
    # Make prediction
    prediction = model.predict(new_data_scaled)
    probability = model.predict_proba(new_data_scaled)
    
    result = "Terima" if prediction[0] == 1 else "Tidak"
    print(f"\nPrediksi untuk mahasiswa baru:")
    print(f"IPK: {ipk}")
    print(f"Penghasilan: {'Rendah' if penghasilan == 0 else 'Sedang' if penghasilan == 1 else 'Tinggi'}")
    print(f"Tanggungan: {tanggungan}")
    print(f"Jarak: {'Dekat' if jarak == 0 else 'Jauh'}")
    print(f"Organisasi: {'Ikut' if organisasi == 1 else 'Tidak'}")
    print(f"UKM: {'Ikut' if ukm == 1 else 'Tidak'}")
    print(f"Jenis Kelamin: {'Perempuan' if gender == 1 else 'Laki-laki'}")
    print(f"SKS: {sks}")
    print(f"Hasil: {result}")
    print(f"Probabilitas: Tidak = {probability[0][0]:.2f}, Terima = {probability[0][1]:.2f}")

def main():
    # Load and process data
    df = load_and_preprocess_data("data_beasiswa.csv")
    
    # Prepare features
    X, y, scaler = prepare_features(df)
    
    # Visualize data
    visualize_data(df)
    
    # Train and evaluate model
    model = train_and_evaluate_model(X, y, scaler)
    
    # Contoh prediksi mahasiswa baru dengan IPK tinggi dan penghasilan rendah
    predict_new_student(
        model=model,
        scaler=scaler,
        ipk=3.75,              # IPK tinggi
        penghasilan=0,         # Penghasilan rendah
        tanggungan=3,          # Jumlah tanggungan
        jarak=0,               # Dekat
        organisasi=1,          # Ikut organisasi
        ukm=1,                 # Ikut UKM
        gender=1,              # Perempuan
        sks=21                 # Jumlah SKS
    )

if __name__ == "__main__":
    main()