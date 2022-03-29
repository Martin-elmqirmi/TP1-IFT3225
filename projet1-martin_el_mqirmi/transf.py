# encoding=utf-8
from bs4 import BeautifulSoup
import argparse
import os
import random as rand

""" Fonction qui récupère le contenu de la boite HTML de la page originale de W3C """
def get_html_text(html):
    pre = html.find_all('pre')
    if len(pre) >= 2:
        text_html = pre[1]
        del text_html['class']
        text = text_html.get_text()
        new_text = swap_text(text)
        return new_text


""" Fonction qui mélange les mots dans les divisions de la boite HTML """
def swap_text(text):
    balise_bool = False
    text_entier = ''
    phrase = ''
    for i in text:
        if i == '<' and not balise_bool:
            tab = phrase.split(' ')
            rand.shuffle(tab)
            new_phrase = ' '.join(tab)
            text_entier += new_phrase
            balise_bool = True
            phrase = ''
        if not balise_bool:
            phrase += i
        else:
            text_entier += i
        if i == '>':
            balise_bool = False
    return text_entier


""" Fonction qui récupère le contenu de la division qui contient
la solution """
def get_html_solution(html):
    div = html.find("div", {"class": "testText"})
    return div


""" Fonction qui récupère le contenu de la boite css des pages W3C """
def get_css_text(html):
    pre = html.find_all('pre')
    if len(pre) >= 2:
        text_css = pre[0]
        del text_css['class']
        return text_css


""" Fonction qui récupère le lien vers le prochain test à visiter """
def get_next_a(html):
    all_a = html.find_all("a", href=lambda href: href and "css3-modsel" in href)
    if len(all_a) == 1 and all_a[0]['href'] != "css3-modsel-d2.html":
        a_next = all_a[0]['href'].split('.')[0] + "test.html"
        return a_next
    elif len(all_a) >= 2:
        a_next = all_a[1]['href'].split('.')[0] + "test.html"
        return a_next
    else:
        return "#"


""" Fonction qui récupère le lien vers le précédent test """
def get_last_a(html):
    all_a = html.find_all("a", href=lambda href: href and "css3-modsel" in href)
    if len(all_a) == 1 and all_a[0]['href'] != "css3-modsel-d2.html":
        return "#"
    else:
        return all_a[0]['href'].split('.')[0] + "test.html"


""" Fonction qui récupère le style css de la page originale W3C """


def get_style_css(html):
    style = html.find("style", {"type": "text/css"})
    del style["type"]
    return style


""" Fonction qui créer une page HTML à partir d'un chemin vers une autre page HTML
et qui met la nouvelle page HTML dans le dossier de sortie passé en paramètre """
def transf(path, out):
    fichier = open(path)
    html = BeautifulSoup(fichier, "html.parser")
    fichierHTML = path.split('/')[len(path.split('/')) - 1]
    url = fichierHTML.split('.')[0]
    testNumber = url.split('-')[len(url.split('-')) - 1]

    fichierSolution = "" + url + "solution.html"
    fichierTest = "" + url + "test.html"

    text_css = get_css_text(html)
    text_html_shuffle = get_html_text(html)
    text_shuffle_without_balise = text_html_shuffle.replace('<', '&lt;').replace('>', '&gt;')
    next_a = get_next_a(html)
    last_a = get_last_a(html)
    style_css = get_style_css(html)
    html_solution = get_html_solution(html)

    page_solution = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
     <meta charset="UTF-8">
        <title>Test {testNumber}</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
           integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css">
        {str(style_css)}
    </head>
    <body>
    <header class="bg-dark">
        <h1 class="text-center p-5 text-white">Testez votre connaissance de CSS</h1>
    </header>
    <main class="container h5 mt-5">
        Lisez le CSS et la structure html du <span class="text-info">test {str(testNumber)}</span> , devinez ce que cela devrait produire, puis cliquez sur le bouton
        <span class="text-danger">Solution</span> pour vérifier votre réponse.
        <hr>
        <nav class="mt-5 navbar bg-info">
            <a href="{str(last_a)}" class="text-white text-decoration-none"> <i class="fas fa-arrow-left"></i> Précédent</a>
            <a href="{str(next_a)}" class="text-white text-decoration-none"> Suivant <i class="fas fa-arrow-right"></i> </a>
        </nav>
        <div class="row mt-5">
            <div class="col-lg-5 border rounded shadow border-info " title="Zone css">
                <div class="p-4">
                    <h3>CSS</h3>
                    <hr>
                    {str(text_css)}
                </div>
            </div>
            <div class="col-lg-5 offset-lg-2 border rounded shadow border-info pr-2" title="Zone html">
                <div class="p-4">
                    <h3>HTML</h3>
                    <hr>
                    {str(text_shuffle_without_balise)}
                </div>
            </div>
        </div>

        <div class="border rounded shadow border-info mt-5 mb-5" title="Zone solution">
            <div class="p-4 text-center">
                <a class="btn btn-success h2" href="{str(url)}test.html" role="button">Revenir</a>
                <hr>
                <div class="text-left">
                    {str(html_solution)}
                </div>
            </div>
        </div>
    </main>
    </body>
    </html>
    """

    page_test = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
         <meta charset="UTF-8">
            <title>Test {testNumber}</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
               integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
            <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css">
        </head>
        <body>
        <header class="bg-dark">
            <h1 class="text-center p-5 text-white">Testez votre connaissance de CSS</h1>
        </header>
        <main class="container h5 mt-5">
            Lisez le CSS et la structure html du <span class="text-info">test {str(testNumber)}</span> , devinez ce que cela devrait produire, puis cliquez sur le bouton
            <span class="text-danger">Solution</span> pour vérifier votre réponse.
            <hr>
            <nav class="mt-5 navbar bg-info">
                <a href="{str(last_a)}" class="text-white text-decoration-none"> <i class="fas fa-arrow-left"></i> Précédent</a>
                <a href="{str(next_a)}" class="text-white text-decoration-none"> Suivant <i class="fas fa-arrow-right"></i> </a>
            </nav>
            <div class="row mt-5">
                <div class="col-lg-5 border rounded shadow border-info " title="Zone css">
                    <div class="p-4">
                        <h3>CSS</h3>
                        <hr>
                        {str(text_css)}
                    </div>
                </div>
                <div class="col-lg-5 offset-lg-2 border rounded shadow border-info pr-2" title="Zone html">
                    <div class="p-4">
                        <h3>HTML</h3>
                        <hr>
                        {str(text_shuffle_without_balise)}
                    </div>
                </div>
            </div>

            <div class="border rounded shadow border-info mt-5 mb-5" title="Zone solution">
                <div class="p-4 text-center">
                    <a class="btn btn-danger h2" href="{url}solution.html" role="button">Solution</a>
                    <hr>
                    <div class="text-left">
                        {str(text_html_shuffle)}
                    </div>
                </div>
            </div>
        </main>
        </body>
        </html>
        """

    if not os.path.exists(out):
        os.makedirs(out)
    solution = open(out + "/" + fichierSolution, "w")
    solution.write(page_solution)
    solution.close()

    test = open(out + "/" + fichierTest, "w")
    test.write(page_test)
    test.close()


if __name__ == "__main__":
    """ Init parser """
    parser = argparse.ArgumentParser()
    """ File name"""
    parser.add_argument('--file_name', type=str)
    """ Repository name """
    parser.add_argument('--repository', type=str)
    args = parser.parse_args()
    file_name = args.file_name
    repository = args.repository
    transf(file_name, repository)
