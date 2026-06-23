# Oral Presentation Script - 7 Minutes Maximum

Project title: Smart Application in Artificial Intelligence and Machine Learning: Study and Understanding  
Professor: EL MKHALET MOUNA  
Student: To be completed

Target rhythm: 14 slides, about 25 to 30 seconds per slide.

## Slide 1 - Project

Good morning/afternoon. My name is [your name], and today I will present my project entitled **Smart Application in Artificial Intelligence and Machine Learning: Study and Understanding**. This project was supervised by Professor **EL MKHALET MOUNA**.


## Slide 2 - Requirements

The project follows strict validation requirements. The application must be executable as a Windows `.exe`, and the first interface must mention EMSI, the professor name, and the student name.

The report follows the official structure from the PDF, and this presentation is designed to stay concise, under seven minutes, while still explaining the essential ideas.

## Slide 3 - Foundation

Artificial intelligence is the field that builds systems able to learn, reason, and support decisions. Machine learning is one of the main components of AI.

Instead of programming every rule manually, machine learning learns patterns from data. In this project, random data is used because it is required by the subject and because it makes experiments controlled and repeatable.

## Slide 4 - Workflow

Each module follows the same scientific workflow.

First, the user chooses parameters with sliders. Second, the application generates random data using `numpy.random.uniform`. Third, the model is trained. Finally, the graph and the metric are displayed together.

This makes the application easy to demonstrate and easy to understand.

## Slide 5 - Architecture

The application is built with a modular desktop architecture.

CustomTkinter provides the graphical interface. Scikit-learn and statsmodels provide the machine learning algorithms. Matplotlib displays the visualizations, and PyInstaller generates the final executable file.

So the project is not only theoretical; it is packaged as a real desktop application.

## Slide 6 - Regression Screenshot

This screenshot shows the regression tab.

The user controls the input ranges and the noise level. The model estimates coefficients and an intercept. The result is evaluated with R2 and RMSE.

R2 explains how much of the variation is captured by the model, while RMSE measures the prediction error.

## Slide 7 - Clustering Screenshot

This slide shows the 3D clustering tab.

K-Means is an unsupervised learning method, so the model does not receive labels. It tries to discover groups in the data. The application generates X1, X2, and X3, then displays the clusters in 3D.

The silhouette score helps evaluate if the clusters are well separated.

## Slide 8 - Classification and Validation Screenshots

Here we can see two other important parts of the application.

Random Forest is used for classification. It gives accuracy and feature importance. Cross-validation compares several models and avoids judging performance from only one split.

This is important because machine learning evaluation must be stable and not based on chance.

## Slide 9 - Modules

The six tabs cover the required machine learning families.

Regression is used for continuous prediction. Clustering is used for unsupervised grouping. Random Forest is used for ensemble classification. ARIMA handles time-series forecasting. The neural network shows non-linear learning, and cross-validation compares model stability.

Together, these modules validate the practical part of the TP.

## Slide 10 - Additional Methods

In the report, I also studied additional methods beyond the application.

SVM creates a margin-based decision boundary. Naive Bayes is a fast probabilistic classifier. Gradient Boosting combines weak learners to improve performance. PCA reduces dimensions. I also discussed DBSCAN, Apriori, Hidden Markov Models, and Autoencoders.

This shows a broader understanding of machine learning.

## Slide 11 - Applications

Machine learning can be applied in the three options.

In development, it can support bug prediction, log analysis, and DevOps monitoring. In cybersecurity, it can detect anomalies, phishing, and suspicious behavior. In artificial intelligence, it supports prediction, segmentation, recognition, and decision support.

So the same ML logic can serve different professional domains.

## Slide 12 - Limits

Machine learning is powerful, but it has limits.

The first limit is data quality. If the data is poor, the model will be poor. Another limit is overfitting, where a model performs well on training data but fails on new data. Models can also drift when real-world data changes.

This is why metrics must always be interpreted with graphs and domain knowledge.

## Slide 13 - Seven-Minute Plan

This presentation is designed to stay under seven minutes.

The first minute covers context, objective, and AI foundations. Around three minutes are for the application workflow, architecture, and screenshots. Two minutes cover methods, domains, limits, and perspectives. The final minute is for conclusion and questions.

This timing keeps the defense clear and controlled.

## Slide 14 - Conclusion

To conclude, this project connects research, implementation, and communication.

The report proves scientific understanding. The executable proves technical implementation. The presentation and video prove communication. Finally, publishing the project on GitHub or LinkedIn can turn it into a professional portfolio project.

Thank you for your attention. I am ready to answer your questions.

## Short Backup Answers

### Why did you use random data?

Because the project requires random data generation, and it makes the application independent from external CSV files.

### Why did you use Python?

Python provides strong libraries for machine learning, visualization, and desktop application development.

### Why is cross-validation important?

Because it evaluates the model across several folds instead of trusting only one train-test split.

### What is the main limitation?

The main limitation is that random data is pedagogical but less realistic than real-world data. A future version could add CSV import and real datasets.
