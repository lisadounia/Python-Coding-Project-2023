# Netflix Content Analysis & Personalized Recommendation System

This project was developed as part of a coding course at **Université catholique de Louvain** with the collaboration of **two other classmates**. It aims to analyze Netflix's content catalog and user ratings to build a **personalized recommendation system**. Using **Python (Pandas, Tabulate)**, we filter, sort, and manipulate the data to optimize content suggestions for users.

Netflix provides thousands of movies and TV shows, and selecting what to watch can be overwhelming. Our system helps users discover content tailored to their preferences using an intelligent **category-based recommendation algorithm**.

## Features

- **Data Analysis & Processing**:
  - Loads and processes Netflix's movie and TV show catalog.
  - Cleans and sorts data for easier manipulation and analysis.

- **User Interaction**:
  - Prompts the user to input preferences based on movies and TV shows they’ve liked.
  - Provides customized recommendations based on genres, directors, actors, and more.

- **Categorization & Matrix Creation**:
  - Builds a matrix of movie/TV show categories based on user preferences.
  - Categories include genres like "Action", "Comedy", "Drama", etc.

- **Recommendation Algorithms**:
  - **Category-based recommendations**: Suggests content based on the most liked genres.
  - **Director and Actor-based suggestions**: Filters based on specific directors or actors.
  - **Parental Control**: Suggests movies and TV shows based on the rating, such as "PG", "R", "TV-MA".
  - **Most Rated**: Displays the highest-rated content for movies and TV shows, by year or overall.

- **Basic Statistics**:
  - Displays statistics about the total number of movies, TV shows, and their distribution by country.
  - Shows how many movies and TV shows each director has produced by nationality.

## Requirements

- **Python 3.x**
- **Pandas**: For data manipulation and analysis.
- **Tabulate**: For displaying data in table format.
- **Pygame** (optional): For future interactive features or extensions.

Install required libraries:
```bash
pip install pandas tabulate pygame
