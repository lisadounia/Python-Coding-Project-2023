import pandas as pd
from tabulate import tabulate

#code source pour listes de catégories (adaptable à n'importe quel colonne ou on souhaite avoir une liste, ex: parentalratings):

#dfcata1=pd.read_csv('netflix_titles.csv')
#dfcatalogue1=dfcata1.copy()

#tv_show_list = []
#movie_list = []

#for index, row in dfcatalogue1.iterrows():
    #categorie = row['listed_in'].split(', ')

    #if row['type'] == 'TV Show':
        #tv_show_list.extend(categorie)
    #elif row['type'] == 'Movie':
        #movie_list.extend(categorie)

#unique_tv_show_cat = list(set(tv_show_list))
#unique_movie_cat = list(set(movie_list))
#print("tvshowlist:", unique_tv_show_cat)
#print("movielist:", unique_movie_cat))


tvshowtypelist = ["Romantic TV Shows","TV Horror","Anime Series", "TV Sci-Fi & Fantasy", "Crime TV Shows","TV Dramas","Korean TV Shows","Stand-Up Comedy & Talk Shows","TV Mysteries","TV Comedies","Docuseries", "Teen TV Shows",
                  "International TV Shows","Reality TV", "Classic & Cult TV", "TV Thrillers", "British TV Shows","TV Shows", "Science & Nature TV","TV Action & Adventure","Spanish-Language TV Shows","Kids' TV"]
movietypelist = ["Anime Features","Dramas","LGBTQ Movies","Movies","Music & Musicals","International Movies","Action & Adventure","Sci-Fi & Fantasy","Documentaries","Romantic Movies", "Children & Family Movies","Sports Movies",
                 "Horror Movies","Faith & Spirituality","Independent Movies","Classic Movies","Thrillers","Comedies","Stand-Up Comedy","Cult Movies"]



cataloguetypelist = tvshowtypelist + movietypelist

# code source pour ce chiffre:
# num_rows_movies = dfmovies.shape[0]
# num_rows_series = dfseries.shape[0]
totaltvshow = 2676
totalmovie = 6131

parentalratings = ["PG-13", "TV-MA", "PG", "TV-14", "TV-PG", "TV-Y", "TV-Y7", "R", "TV-G", "G", "NC-17", "NR", "TV-Y7-FV", "UR"]

def save_results_to_csv(df, filename):
#Fonction qui permet de demander à l'utilisateur s'il veut enregistrer ses modifications
    while True:
        save_option = input('Do you want to save the result to a CSV file? (yes/no): ').lower()
        if save_option == 'yes':
            save_name = filename + '.csv'
            df.to_csv(save_name, index=False)
            print('Data saved to',save_name)
            break
        elif save_option == 'no':
            print('Result not saved.')
            break
        else:
            print('Error, please enter "yes" or "no".')


def gofind(what,where,df):
#cette fonction permet de chercher l'élément 'what' dans la collonne 'where' d'un certain dataframe, 'df'
    what=what.lower()
    dfgofind = df[df[where].str.lower().apply(lambda x: any(what in item for item in str(x).split(',') if isinstance(x, str)))]
    return dfgofind

def displaydf(df):
#Cette fonction permet un bel affichage des dataframe
#Vérifier si df est une série grâce à isinstance qui vérifie si un objet est une instance d'une classe spécifique.
#Permet l'affichage des recommendations qui sont des series pandas
    if isinstance(df, pd.Series):
        # Transformer la série en un DataFrame avec un nom de colonne générique
        df = pd.DataFrame(df)
        # Inverser lignes et colonnes
        df = df.transpose()
        # Afficher le DataFrame généré
        df = df.set_index(df.columns[0])
        print(tabulate(df, headers='keys', tablefmt='pretty'))
        print()
    else:
        # Définir la première colonne comme index sans connaître son nom pour éviter l'indexage par défaut de pandas
        df.set_index(df.columns[0], inplace=True)
        # Si le DataFrame a moins de 1000 lignes, l'afficher entièrement
        if len(df) <= 1000:
            print(tabulate(df, headers='keys', tablefmt='pretty'))
            print()
       #Afficher le dataframe par tranche de 1000
        else:
            chunk_size = 1000
            row = len(df)
            for start in range(0, row, chunk_size):
                chunk = df.iloc[start:start + chunk_size]
                print(tabulate(chunk, headers='keys', tablefmt='pretty'))
                print()

            # Afficher le reste des lignes s'il y en a
            remainder = row % chunk_size
            if remainder != 0:
                last_chunk = df.tail(remainder)
                print(tabulate(last_chunk, headers='keys', tablefmt='pretty'))
                print()

def choice():
#Fonction qui demande à l'utilisateur de choisir les options de tri pour un catalogue de films et/ou de séries
  print('Do you want to sort:\n')
  print('1.The whole catalog')
  print('2.Only movies')
  print('3.Only series')
  while True:
    choice=input().strip()
    if choice not in ['1','2','3']:
      print('Error, enter a number in the given propositions\n')
    else:
      return choice

def by_year(dfcatalogue,dfmovies,dfseries):
#Fonction qui trie un catalogue de films et/ou de séries par année de sortie
  answer=choice()
  if answer=='1':
    dfsorted=dfcatalogue.sort_values(by='release_year')
  elif answer=='2':
    dfsorted=dfmovies.sort_values(by='release_year')
  elif answer=='3':
    dfsorted=dfseries.sort_values(by='release_year')
  return dfsorted


def by_country(dfcatalogue,dfmovies,dfseries):
#Fonction qui trie un catalogue de films et/ou de séries par pays
  answer=choice()
  if answer=='1':
    dfsorted=dfcatalogue.sort_values(by='country')
  elif answer=='2':
    dfsorted=dfmovies.sort_values(by='country')
  elif answer=='3':
    dfsorted=dfseries.sort_values(by='country')
  return dfsorted

def by_type(dfcatalogue,dfmovies,dfseries):
#Fonction qui filtre le catalogue de films et/ou de séries par genre
  answer=choice()
  print('Here are the possible types:')
  if answer=='1':
    dfsorted=dfcatalogue
    print(cataloguetypelist)
  elif answer=='2':
    dfsorted=dfmovies
    print(movietypelist)
  elif answer=='3':
    dfsorted=dfseries
    print(tvshowtypelist)
  i=input('Enter the type that you want')

  df=gofind(i,'listed_in',dfsorted)
  if df.empty :
    print("This type was not found")
    menu(cataloguetypelist)
  else:
    return df

def by_type_duration(dfcatalogue,dfmovies,dfseries):
#Fonction qui va trier les films en fonction de leur durée (min) et les séries en fonction du nombre de saisons. Si l'utilisateur choisi de voir le catalogue en entier les films vont s'afficher en premier suivis des séries (un film étant toujours plus court qu'une saison)
  df=by_type(dfcatalogue,dfmovies,dfseries).copy()

  # Cree une colonne film_duration qui met en minute si la 'duration' en minutes et si en 'seasons' met en infini
  df.loc[:, 'film_duration'] = df['duration'].apply(lambda x: int(x.split(' ')[0]) if 'Season' not in x else float('inf'))

  # on trie film_duration, on aura tous les films triés et puis les series car égale à infinie et ensuite on trie duration, il va mettre les seasons par odre chronologique
  df = df.sort_values(by=['film_duration', 'duration'])
  # on supprime colomne film_duration une fois qu'elle à servie
  dfsorted = df.drop('film_duration', axis=1)
  if dfsorted.empty :
    print("This type was not found")
    menu(cataloguetypelist)
  else:
    return dfsorted


def by_director_year(dfcatalogue, dfmovies, dfseries):
#Fonction qui va demander à l'utilisateur quel directeur il souhaite voir et la fonction va lui retourner tous les films/séries ou le directeur apparait avec les résultats triés par année
    director_name = input("Enter the director's name: ").strip()
    df_director=gofind(director_name,'director',dfcatalogue)
    answer = choice()
    if answer == '1':
        dfsorted = dfcatalogue[dfcatalogue['title'].isin(df_director['title'])].sort_values(by=['release_year'])
    elif answer == '2':
        dfsorted = dfmovies[dfmovies['title'].isin(df_director['title'])].sort_values(by=['release_year'])
    elif answer == '3':
        dfsorted = dfseries[dfseries['title'].isin(df_director['title'])].sort_values(by=['release_year'])
    if dfsorted.empty :
      print("No movies or series found for",director_name)
      menu(cataloguetypelist)
    else :
      return dfsorted

def by_actor_year(dfcatalogue, dfmovies, dfseries):
#Fonction qui va demander à l'utilisateur quel acteur il souhaite voir et la fonction va lui retourner tous les films/séries ou l'acteur apparait avec les résultats triés par année
    actor_name = input("Enter the actor's name: ").strip()
    df_actor=gofind(actor_name,'cast',dfcatalogue)
    answer = choice()
    if answer == '1':
        dfsorted = dfcatalogue[dfcatalogue['title'].isin(df_actor['title'])].sort_values(by=['release_year'])
    elif answer == '2':
        dfsorted = dfmovies[dfmovies['title'].isin(df_actor['title'])].sort_values(by=['release_year'])
    elif answer == '3':
        dfsorted = dfseries[dfseries['title'].isin(df_actor['title'])].sort_values(by=['release_year'])
    if dfsorted.empty :
          print("This actor was not found")
          menu(cataloguetypelist)
    else:
      return dfsorted

def by_director_and_type(dfcatalogue, dfmovies, dfseries):
#Fonction qui trie par réalisateur et par catégorie
    director_name = input("Enter the director's name: ").strip()
    df_director=gofind(director_name,'director',by_type(dfcatalogue, dfmovies, dfseries))
    if df_director.empty :
          print("This type or director was not found")
          menu(cataloguetypelist)
    else:
      return df_director

def by_actor_and_type(dfcatalogue, dfmovies, dfseries):
#Fonction qui trie par acteur et par catégorie
    cast_name = input("Enter the cast's name: ").strip()
    df_cast=gofind(cast_name,'cast',by_type(dfcatalogue, dfmovies, dfseries))

    if df_cast.empty:
        print("No movies or series found for cast ",cast_name,"or the spelling of the actor's name is incorrect or type was not found")
        menu(cataloguetypelist)
    else:
      return df_cast


def rating(df):
#Fonction qui calcule la note moyenne des films/séries dans un dataframe
    df = df.copy()
    #on laisse toutes les colonnes show_id
    ratings_columns = df.drop('show_id', axis=1)
    #Calcul de la somme des notes comptabilisé pour chaque film/series
    df['sum'] = ratings_columns.iloc[:, :].sum(axis=1)
    #compte la note pour ce film/serie différente de 0
    df['vote_count'] = ratings_columns.iloc[:, :].apply(lambda row: (row != 0).sum(), axis=1)
    df['average_rate'] = df['sum'] / df['vote_count']
    return df

def most_rated(dfcatalogue,dfmovies,dfseries,df_ratings):
#Fonction qui permet d'obtenir les films/séries les mieux notés
    answer = choice()
    if answer == '1':
        df=dfcatalogue
        show_ids = df.loc[df['type'].isin(['TV Show', 'Movie']), 'show_id']
    elif answer == '2':
        df= dfmovies
        show_ids = df.loc[df['type'] == 'Movie', 'show_id']
    elif answer == '3':
        df = dfseries
        show_ids = df.loc[df['type'] == 'TV Show', 'show_id']
    dfunsorted=df_ratings[df_ratings['show_id'].isin(show_ids)]
    dfsorted=rating(dfunsorted)
    dfsorted=pd.merge(df,dfsorted, on='show_id')
    dfsorted=dfsorted.sort_values(by='average_rate',ascending=False)
    return dfsorted


def most_rated_year(dfcatalogue,dfmovies,dfseries,df_ratings):
#Fonction qui permet d'obtenir les films/séries les mieux notés pour une année spécifique
    df=most_rated(dfcatalogue,dfmovies,dfseries,df_ratings)
    while True:
        try :
            print('Which year do you want to filter with ?')
            i=int(input())
            i=str(i)
            break
        except ValueError:
            print('Enter a valid year')
    df['release_year']=df['release_year'].astype('string')
    dfsorted=gofind(i,'release_year' , df)
    if dfsorted.empty :
          print("This year was not found or is not valid")
          menu(cataloguetypelist)
    else:
      return dfsorted

def most_rated_recent(dfcatalogue,dfmovies,dfseries,df_ratings):
#Fonction qui permet d'obtenir les films/séries les mieux notés récemment, elle trie le DataFrame par année de sortie et note la moyenne de manière décroissante.
    df=most_rated(dfcatalogue,dfmovies,dfseries,df_ratings)
    dfsorted = df.sort_values(['release_year','average_rate'], ascending=[False,False])
    return dfsorted

def parental_control(dfcatalogue):
#fonction qui permet de trier les film/série en fonction d'une classification parentale demandée
  df=dfcatalogue
  print(parentalratings)
  i=input('Enter the parental controll that you want').strip()
  df=gofind(i,'rating',df)
  if df.empty :
        print("This type or director was not found")
        menu(cataloguetypelist)
  else:
    return df


def show(dfcatalogue,dfmovies,dfseries,df_ratings,cataloguetypelist):
#Fonction qui crée un menu permettant d'afficher les différentes options que l'utilisateur peut choisir entre les 'Show'
#les ilocs dans certaines lignes de code sont la pour sélectionner des colonnes spécifiques du DataFrame
  print('0.Return to menu\n')
  print('1.Show the movies in the catalog\n')
  print('2.Show the series in the catalog\n')
  print('3.Sort and show the movies and/or the series by release years\n')
  print('4.Show the movies and/or series by country\n')
  print('5.Show the movies and/or the series by type (romantic, action, drama...)\n')
  print('6.Show the movies and/or the series by type (romantic, action, drama...) and sort them by duration\n')
  print('7.Show the movies and/or series carried out by a specific director and sort them by year\n')
  print('8.Show the movies and/or series carried out by a specific actor and sort them by year\n')
  print('9.Show how many movies and/or series a director carried out of a specific type (e.g., romantic,science fiction, triller...)\n')
  print('10.Show the movies and/or series of a specific type (e.g., romantic, action, drama...) played by a specific actor\n')
  print('11.Show the most rated movies and/or series\n')
  print('12.Show the most rated movies and/or series in a specific year\n')
  print('13.Show the most rated and recent movies and/or series\n')
  print("14.Show the movies and series of according to a specific parental control code (e.g., 'PG-13','TV-MA', 'PG', 'TV-14', ‘TV-PG’)\n")

  i=input('Enter a number in the given propositions\n')
  if i not in ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14']:
    print('Error, enter a number in the given propositions\n')
    show(dfcatalogue,dfmovies,dfseries,df_ratings,cataloguetypelist)
  else:
      if i == '0':
          menu(cataloguetypelist)

      if i == '1':
          displaydf(dfmovies)
          save_results_to_csv(dfmovies, "movies_result")

      elif i == '2':
          displaydf(dfseries)
          save_results_to_csv(dfseries, "series_result")

      elif i == '3':
          df_sorted_by_year = by_year(dfcatalogue, dfmovies, dfseries).iloc[:, [2, 7]]
          displaydf(df_sorted_by_year)
          save_results_to_csv(df_sorted_by_year, "by_year_result")

      elif i == '4':
          df_sorted_by_country = by_country(dfcatalogue, dfmovies, dfseries).iloc[:, [2, 5]]
          displaydf(df_sorted_by_country)
          save_results_to_csv(df_sorted_by_country, "by_country_result")

      elif i == '5':
          df_sorted_by_type = by_type(dfcatalogue, dfmovies, dfseries).iloc[:, [2, 10]]
          displaydf(df_sorted_by_type)
          save_results_to_csv(df_sorted_by_type, "by_type_result")

      elif i == '6':
          df_sorted_by_type_duration = by_type_duration(dfcatalogue, dfmovies, dfseries).iloc[:, [2, 9, 10]]
          displaydf(df_sorted_by_type_duration)
          save_results_to_csv(df_sorted_by_type_duration, "by_type_duration_result")

      elif i == '7':
          df_sorted_director_year = by_director_year(dfcatalogue, dfmovies, dfseries).iloc[:, [2, 3, 7]]
          displaydf(df_sorted_director_year)
          save_results_to_csv(df_sorted_director_year, "by_director_year_result")

      elif i == '8':
          df_sorted_actor_year = by_actor_year(dfcatalogue, dfmovies, dfseries).iloc[:, [2, 4, 7]]
          displaydf(df_sorted_actor_year)
          save_results_to_csv(df_sorted_actor_year, "by_actor_year_result")

      elif i == '9':
          df_sorted_director_and_type = by_director_and_type(dfcatalogue, dfmovies, dfseries).iloc[:, [2, 3, 10]]
          displaydf(df_sorted_director_and_type)
          save_results_to_csv(df_sorted_director_and_type, "by_director_and_type_result")

      elif i == '10':
          dfsorted_by_actor_type = by_actor_and_type(dfcatalogue, dfmovies, dfseries).iloc[:, [2, 4, 10]]
          displaydf(dfsorted_by_actor_type)
          save_results_to_csv(dfsorted_by_actor_type, "by_actor_and_type_result")

      elif i == '11':
          df_sorted_most_rated = most_rated(dfcatalogue, dfmovies, dfseries, df_ratings).iloc[:, [2, 114]]
          displaydf(df_sorted_most_rated)
          save_results_to_csv(df_sorted_most_rated, "most_rated_result")

      elif i == '12':
          df_sorted_most_rated_year = most_rated_year(dfcatalogue, dfmovies, dfseries, df_ratings).iloc[:, [2, 7, 114]]
          displaydf(df_sorted_most_rated_year)
          save_results_to_csv(df_sorted_most_rated_year, "most_rated_year_result")

      elif i == '13':
          df_sorted_most_rated_recent = most_rated_recent(dfcatalogue, dfmovies, dfseries, df_ratings).iloc[:,[2, 7, 114]]
          displaydf(df_sorted_most_rated_recent)
          save_results_to_csv(df_sorted_most_rated_recent, "most_rated_recent_result")

      elif i == '14':
          df_sorted_by_parental = parental_control(dfcatalogue).iloc[:, [2, 8]]
          displaydf(df_sorted_by_parental)
          save_results_to_csv(df_sorted_by_parental, "parental_controll_result")

      menu(cataloguetypelist)

def nationality_directors_count(dfcatalogue):
#Fonction qui compte le nombre de films réalisés en fonction de la nationalité des directeurs et affiche donc le nombre regroupé par pays
  df = dfcatalogue
  df = df.dropna(subset=['director'])
  df = df.dropna(subset=['country'])
  df['country'] = df['country'].str.split(',')
  df = df.explode('country')
  df['country']=df['country'].str.strip()
  country_movie_counts = df['country'].value_counts().reset_index()
  country_movie_counts.columns = ['country', 'movie_count']
  recreated_df = pd.merge(df, country_movie_counts, on='country', how='inner')
  recreated_df = recreated_df.sort_values(['movie_count','country'], ascending=[False,False])
  return recreated_df

def basic_stats(dfcatalogue,dfmovies,dfseries):
#Fonction qui affiche des statistiques de base sur le catalogue, notamment le nombre totale de films et de séries
#Elle indique également le nombre de films et série émanant de chaque pays
  print("here are the basic statistics:\n")
  num_rows_movies = dfmovies.shape[0]
  num_rows_series = dfseries.shape[0]
  statistics_data = {'Statistic': ['Number of Movies', 'Number of Series'],'Count': [num_rows_movies, num_rows_series]}
  statistics_df = pd.DataFrame(statistics_data)
  displaydf(statistics_df)
  if num_rows_movies > num_rows_series:
    print ("there are more movies than series\n")
  else:
      print("there are more series than movies\n")
      print()

  df = dfcatalogue['country'].str.split(',',expand=True).stack().reset_index(level=1, drop=True).reset_index(name='country')
  df = df.dropna(subset=['country'])
  df['country']=df['country'].str.strip()
  country_counts = df['country'].value_counts().reset_index()
  country_counts.columns = ['country', 'count']
  country_counts = country_counts.sort_values(by='count', ascending=False)
  countries_data = country_counts.rename(columns={'count': 'Number of Productions'})
  countries_df = pd.DataFrame(countries_data)
  print("here is a list of the countries and the number of movies/series produced\n")
  displaydf(countries_df)

def cat_matrix(dfcatalogue):
#crée une matrice remplie de 0 en fonction du nombre de catégorie de films/série. La ligne 0 est occupée par la liste de catégorie et les position 0 à l'horizontale aussi
  lencat=len(cataloguetypelist)+1
  matrix=[[0]*lencat for i in range(lencat)]
  matrix[0]=['']+cataloguetypelist
  for i in range(1,lencat):
    matrix[i][0]=cataloguetypelist[i-1]
  return matrix

def find_index(liste,cataloguetypelist):
#trouve l'indince d'une certaine catégorie dans la liste des catégories
  index_list = []
  for i in liste:
    i=i.strip()
    index=cataloguetypelist.index(i)+1
    index_list.append(index)
  return index_list



def fill_matrix(dfcatalogue,cataloguetypelist):
#remplis la matrice créée par les informations retrouvé dans le catalogue
  matrix_base=cat_matrix(dfcatalogue)
  df = dfcatalogue
  #supprime les 'listed_in' vide
  df = df.dropna(subset=['listed_in'])
  #coupe la string des catégories de chaque film en foncion de la virgule
  df['listed_in'] = df['listed_in'].str.split(',')
  for i in df['listed_in']:
    #trouve l'index de la catégorie en question i
    index_list = find_index(i,cataloguetypelist)
    #rajoute 1 à l'endroit des coordoné i à chaque fois que la catégorie est trouvé
    for j in index_list:
      for k in index_list:
        matrix_base[j][k]+=1

  return matrix_base



def recommend_top_types1(liked_list, df_not_watched):
    # Extrait les 5 premiers éléments de liked_list
    top_types = liked_list[:5]

    df_not_watched1=df_not_watched.copy()

    # Compte les occurrences de chaque type dans la colonne spécifiée pour chaque ligne
    df_not_watched1["type_counts"] = df_not_watched1["listed_in"].apply(lambda x: sum(1 for t in top_types if t in [type.strip() for type in x.split(',')]))
    sorted_df = df_not_watched1.sort_values(by="type_counts", ascending=False)

    return sorted_df

def recommend_top_types2(liked_list, df_not_watched):
    # Extrait les 5 premiers éléments de liked_list
    top_types = liked_list[:5]

    df_not_watched2=df_not_watched.copy()

    # Compte les occurrences de chaque type dans la colonne spécifiée pour chaque ligne
    df_not_watched2["type_counts"] = df_not_watched2["listed_in"].apply(lambda x: sum(1 for t in top_types if t[0] in [type.strip() for type in x.split(',')] and t[1] in [type.strip() for type in x.split(',')]))
    sorted_df = df_not_watched2.sort_values(by="type_counts", ascending=False)

    return sorted_df

def recommend_top_types3(liked_list, df_not_watched):
    # Extrait les 5 derniers éléments de liked_list
    top_types = liked_list[5:]

    df_not_watched3=df_not_watched.copy()

    # Compte les occurrences de chaque type dans la colonne spécifiée pour chaque ligne
    df_not_watched3["type_counts"] = df_not_watched3["listed_in"].apply(lambda x: sum(1 for t in top_types if t in [type.strip() for type in x.split(',')]))
    sorted_df = df_not_watched3.sort_values(by="type_counts", ascending=False)

    return sorted_df


def recom1(matrix_liked, df_title_not_watched, nlikedtvshow, nlikedmovie):
    liked_list = []
    for i in range(1, len(matrix_liked)):
        # nombre de show liké et nom du type
        combi = (matrix_liked[i][i], matrix_liked[0][i])
        liked_list.append(combi)
    tvshow_list = liked_list[:23]
    movie_list = liked_list[23:]
    tvshow_list = sorted(tvshow_list, reverse=True)
    movie_list = sorted(movie_list, reverse=True)

    # refaire une liste sans les notes attribuées au genre
    tvshow_list = [tup[1] for tup in tvshow_list]
    movie_list = [tup[1] for tup in movie_list]

    ptvshow = (nlikedtvshow / totaltvshow) * 100
    pmovie = (nlikedmovie / totalmovie) * 100


    # pourcentage de regardage des films/tvshow et comparaison, si plus de 1% de dif on recommande
    if pmovie - ptvshow < -1:
        print("You prefer TV shows, here are 2 recommendations")
        dfrecom = recommend_top_types1(tvshow_list, df_title_not_watched).iloc[:2, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)
    elif ptvshow - pmovie < -1:
        print("You prefer Movies, here are 2 recommendations")
        dfrecom = recommend_top_types1(movie_list, df_title_not_watched).iloc[:2, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)

    else:
        print('tvshow :')
        dfrecom = recommend_top_types1(tvshow_list, df_title_not_watched).iloc[0, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)
        print('movie :')
        dfrecom = recommend_top_types1(movie_list, df_title_not_watched).iloc[0, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)


def recom2(matrix_liked, df_title_not_watched, nlikedtvshow, nlikedmovie):
    # creer une matrice pour tvshow
    matrix_liked_tvshows = matrix_liked[:23]
    for i in range(len(matrix_liked_tvshows)):
        matrix_liked_tvshows[i] = matrix_liked_tvshows[i][:23]

    # creer une matrice pour movie
    matrix_liked_movie = matrix_liked[23:]
    for i in range(len(matrix_liked_movie)):
        matrix_liked_movie[i] = [matrix_liked_movie[i][0]] + matrix_liked_movie[i][23:]
    movietypelistbis = [""] + movietypelist
    matrix_liked_movie = [movietypelistbis] + matrix_liked_movie

    tvshows_liked_combi, movie_liked_combi = [], []
    rows_tv = len(matrix_liked_tvshows)
    columns_tv = len(matrix_liked_tvshows[0])
    rows_movie = len(matrix_liked_movie)
    columns_movie = len(matrix_liked_movie[0])

    for i in range(1, rows_tv):
        for j in range(1, columns_tv):
            if i > j:
                tuple_rate_combi = (matrix_liked_tvshows[i][j], matrix_liked_tvshows[0][i], matrix_liked_tvshows[j][0])
                tvshows_liked_combi.append(tuple_rate_combi)

    for i in range(1, rows_movie):
        for j in range(1, columns_movie):
            if i > j:
                tuple_rate_combi = (matrix_liked_movie[i][j], matrix_liked_movie[0][i], matrix_liked_movie[j][0])
                movie_liked_combi.append(tuple_rate_combi)

    tvshows_liked_combi = sorted(tvshows_liked_combi, reverse=True)
    movie_liked_combi = sorted(movie_liked_combi, reverse=True)

    tvshows_liked_combi = [(t[1], t[2]) for t in tvshows_liked_combi]
    movie_liked_combi = [(t[1], t[2]) for t in movie_liked_combi]

    tvshows_liked_combi = [list(item) for item in tvshows_liked_combi]
    movie_liked_combi = [list(item) for item in movie_liked_combi]

    ptvshow = (nlikedtvshow / totaltvshow) * 100
    pmovie = (nlikedmovie / totalmovie) * 100

    # pourcentage de visionage des films/tvshow et comparaison, si plus de 1% de dif on recommande (user 40 TVshow, user 45movies)
    if ptvshow - pmovie > 1:
        print("You prefer TV shows, here are 2 recommendations")

        dfrecom = recommend_top_types2(tvshows_liked_combi, df_title_not_watched).iloc[:2, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)
    elif ptvshow - pmovie < -1:
        print("You prefer Movies, here are 2 recommendations")
        dfrecom = recommend_top_types2(movie_liked_combi, df_title_not_watched).iloc[:2, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)
    else:
        print('tvshow :')
        dfrecom = recommend_top_types2(tvshows_liked_combi, df_title_not_watched).iloc[0, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)
        print('movie :')
        dfrecom = recommend_top_types2(movie_liked_combi, df_title_not_watched).iloc[0, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)


def recom3(matrix_liked, df_title_not_watched, nlikedtvshow, nlikedmovie):
    # même commencement que recom1 : on trie la liste des types de films et series du plus aimeé au moins aimé
    liked_list = []
    for i in range(1, len(matrix_liked)):
        # nombre de show liké et nom du type
        combi = (matrix_liked[i][i], matrix_liked[0][i])
        liked_list.append(combi)
    tvshow_list = liked_list[:23]
    movie_list = liked_list[23:]
    tvshow_list = sorted(tvshow_list, reverse=True)
    movie_list = sorted(movie_list, reverse=True)

    # on eleve les tuples qui ont un score de 0
    for i in range(len(tvshow_list)-1):
        if tvshow_list[i][0] == 0:
            tvshow_list.pop(i)
    for i in range(len(movie_list)-1):
        if movie_list[i][0] == 0:
            movie_list.pop(i)

    tvshow_list = [tup[1] for tup in tvshow_list]
    movie_list = [tup[1] for tup in movie_list]

    ptvshow = (nlikedtvshow / totaltvshow) * 100
    pmovie = (nlikedmovie / totalmovie) * 100

    if ptvshow - pmovie > 1:
        print("You prefer TV shows but we suggest 2 Movies to expand your horizons")
        dfrecom = recommend_top_types3(movie_list, df_title_not_watched).iloc[:2, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)
    elif ptvshow - pmovie < -1:
        print("You prefer Movies but we suggest 2 TV shows to expand your horizons")
        dfrecom = recommend_top_types3(tvshow_list, df_title_not_watched).iloc[:2, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)
    else:
        print('tvshow :')
        dfrecom = recommend_top_types3(tvshow_list, df_title_not_watched).iloc[0, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)
        print('movie :')
        dfrecom = recommend_top_types3(movie_list, df_title_not_watched).iloc[0, [2, 7, 9, 10, 11]]
        displaydf(dfrecom)

def user_df(dfcatalogue, df_ratings):
  while True:
    try:
        i = int(input("What's your user ID? \n"))
        if 0 < i <= 100:
            break
        else:
            print("Error, enter a valid user ID between 1 and 100")
    except ValueError:
        print("Error, enter a valid user ID ")

  i=str(i)

  df_id=df_ratings[["show_id",i]]

  #Nous considérons qu'un film/série aimé représente une note d'au minimum 3/5 donc nous enlevons tout les film/série ne respectant pas cette condition
  row_not_condition=df_id[df_id[i]<3].index
  dfliked= df_id.drop(row_not_condition)

 #Nous recréons un catalogue à partir de l'original gardant uniquement films/série dont la note est > à 3/5
  df_title_liked=dfcatalogue[dfcatalogue['show_id'].isin(dfliked['show_id'])]


  #Nous recréons un catalogue à partir de l'original gardant uniquement films/série non regarder
  row_not_condition2=df_id[df_id[i]>0].index
  df_not_watchedog=df_id.drop(row_not_condition2)
  df_not_watched=df_not_watchedog.copy()
  df_title_not_watched=dfcatalogue[dfcatalogue['show_id'].isin(df_not_watched['show_id'])]




  #à partir du nouveau catalogue des films regarder, création d'un matrice de genre propre à l'utilisateur
  matrix_liked=fill_matrix(df_title_liked,cataloguetypelist)

  #Nous comptons le nombre de série et film respectivement regarder pour pouvoir affiner les futurs recommendations
  nlikedmovie = df_title_liked[df_title_liked['type'] == 'Movie'].shape[0]
  nlikedtvshow = df_title_liked[df_title_liked['type'] == 'TV Show'].shape[0]

  #appel des diférentes fonction de recommendation
  print("First recommendation")
  recom1(matrix_liked,df_title_not_watched,nlikedtvshow,nlikedmovie)
  print()
  print("Second recommendation")
  recom2(matrix_liked,df_title_not_watched,nlikedtvshow,nlikedmovie)
  print()
  print("Third recommendation")
  recom3(matrix_liked,df_title_not_watched,nlikedtvshow,nlikedmovie)



def menu_recom(dfcatalogue, df_ratings,cataloguetypelist):
#Fontion qui crée un menu propre aux recommandations
  print('What do you want to do ?\n')
  print('0.Return to menu\n')
  print('1.Show the matrix of categories\n')
  print('2.Show suggestions\n')
  while True:
    i=input()
    if i not in ['0','1','2']:
      print('Error, enter a number in the given propositions\n')
    else:
      break

  if i=='0':
    return menu(cataloguetypelist)

  elif i=="1":
    matrix=fill_matrix(dfcatalogue,cataloguetypelist)
    #utilisation de la librairie tabulate pour l'affichage en tableau
    #"firstrow":première ligne de la matrice sera utilisée comme en-têtes de colonnes. "pretty" est utilisé pour obtenir une table joliment formatée.
    table = tabulate(matrix, headers="firstrow", tablefmt="pretty")
    print(table,"\n")

  elif i=="2":
    user_df(dfcatalogue,df_ratings)


def menu(cataloguetypelist):
#Fonction créant le menu principale, c'est elle qui est rappellé à la fin de chaque fonction
  dfcata=pd.read_csv('netflix_titles.csv')
  dfcatalogue=dfcata.copy()
  df_ratings = pd.read_csv('ratings.csv')
  dfmovies=dfcatalogue[dfcatalogue['type'].apply(lambda x:'Movie' in x)]
  dfseries=dfcatalogue[dfcatalogue['type'].apply(lambda x:'TV Show' in x)]
  print('What do you want to do ?\n')
  print('0.To stop the program\n')
  print('1.Show catalog\n')
  print('2.List the nationality of the directors\n')
  print('3.Basic Statistics\n')
  print('4.Recommendation\n')
  print()

  while True:
    i=input('Enter a number in the given propositions\n')
    if i not in ['0','1','2','3','4']:
      print('Error, enter a number in the given propositions\n')
    else:
      break

  if i=='0':
    return

  elif i=="1":
    show(dfcatalogue,dfmovies,dfseries,df_ratings,cataloguetypelist)

  elif i=="2":
    df_sorted_nationality_directors_count = nationality_directors_count(dfcatalogue).iloc[:, [2, 3, 5]]
    displaydf(df_sorted_nationality_directors_count)
    save_results_to_csv(df_sorted_nationality_directors_count, "by_nationality_director_result")

  elif i=="3":
    basic_stats(dfcatalogue,dfmovies,dfseries)

  elif i=="4":
    menu_recom(dfcatalogue, df_ratings,cataloguetypelist)

  menu(cataloguetypelist)



menu(cataloguetypelist)
