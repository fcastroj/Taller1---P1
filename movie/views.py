from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from .models import Movie
# Create your views here.

def home(request):
    # return HttpResponse('<h1>Welcome to home Page</h1>')
    # return render(request, 'home.html')
    # return render(request, 'home.html', {'name': 'Felipe Castro Jaimes'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') # Obtener todos los años de las películas
    movie_counts_by_year = {} # Crear un diccionario para almacenar la cantidad de películas por año
    for year in years: # Contar la cantidad de películas por año
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5 # Ancho de las barras
    bar_spacing = 0.5 # Separación entre las barras
    bar_positions = range(len(movie_counts_by_year)) # Posiciones de las barras

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

        # Obtener el primer género de cada película
    genres = Movie.objects.values_list('genre', flat=True)
    
    movie_counts_by_genre = {}
    for genre_list in genres:
        if genre_list:  # Verifica que la película tenga al menos un género
            first_genre = genre_list.split(',')[0].strip()  # Toma solo el primer género
            movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1

    # Crear gráfica de barras para géneros
    plt.figure(figsize=(10, 5))
    plt.bar(movie_counts_by_genre.keys(), movie_counts_by_genre.values(), color='skyblue')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(rotation=45, ha='right')
    
    # Guardar la gráfica en base64
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png_genre = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_png_genre).decode('utf-8')

    # Pasar ambas gráficas a la plantilla
    return render(request, 'statistics.html', {'graphic': graphic, 'graphic_genre': graphic_genre})


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email}) 