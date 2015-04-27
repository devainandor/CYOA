import string
import sys
import random
import os
import re

section_template = """
<section id="s{}">
<p>{}</p>
{}
<ul>
{}</ul>
</section>

"""

choice_template = '<li class="to" data-to="s{}">{}</li>\n'

image_template = '<div class="illustration" style="background-image: url({});"></div>'

def generate_adventure_id():
    while True:
        adventure_id = ''.join(random.sample(string.ascii_letters, 8))
        if not os.path.exists(adventure_id + '.html'):
            return adventure_id

source = open(sys.argv[1], 'r', encoding='utf-8')
adventure_id = generate_adventure_id()
outfile_name = adventure_id + '.html'
outfile = open(outfile_name, 'w', encoding='utf-8')
outfile.write("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title></title>
</head>
<body>
<link href='http://fonts.googleapis.com/css?family=Sorts+Mill+Goudy&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
<link rel="stylesheet" type="text/css" href="style.css">
<script type="text/javascript" src="jquery-2.1.3.min.js"></script>
<nav>
<a href="/">All games</a>
<a href="/about.html">About</a>
•
<span id="restart">Restart game</span>
<!--
<span id="current">Link to current chapter</span>
<a id="current_a" href="">Link to current chapter</a>
-->
</nav>
<div id="container">
""")

source_content = source.read()
meta = source_content.split('\n\n')[0]
author, title = meta.split(':')

outfile.write("""
<h2>{}</h2>
<h1>{}</h1>

""".format(author, title))

for section in source_content.split('\n\n')[1:]:
    section_id, content = section.split('\n', 1)
    description = ''
    choices = ''
    image = ''
    for line in content.split('\n'):
        if re.match('\d+:', line):
            to, text = line.split(':')
            choices = choices + choice_template.format(to, text)
        elif re.match('\(.*\)', line):
            image = image_template.format(line[1:-1])
        else:
            description = description + line + ' '
    outfile.write(section_template.format(
        section_id.replace('.', ''), 
        description,
        image,
        choices
    ))

outfile.write("""

</div><!-- #container -->

<script type="text/javascript">
$(document).ready(function () {
    var adventureID = '""")
outfile.write(adventure_id)
outfile.write("""';
    var lastSection = localStorage.getItem(adventureID + '_lastSection');
    if (lastSection == null) {
        lastSection = 's1';
        localStorage.setItem(adventureID + '_lastSection', 's1');
    }
    $('#' + lastSection).show();

    $('.to').on('click', function() { 
        var el = $('#' + $(this).data('to'))
        el.show();
        $('html, body').animate({
            scrollTop: $(this).offset().top - $('nav').height() - 50
        }, 1000);
        $(this).addClass('selected');
        $(this).parent().children().off('click');
        $(this).parent().children().addClass('inactive');
        localStorage.setItem(adventureID + '_lastSection', $(this).data('to'));
        $('#current_a').hide();
        $('#current').show();
    });

    $('#restart').on('click', function() {
        if (confirm('If you restart you will lose all progress!')) {
            localStorage.setItem(adventureID + '_lastSection', 's1');
            location.reload();
        }
    });
    
    //$('#current').on('click', function() {
    //    var currentChapterHref = adventureID + '.html#' + localStorage.getItem(adventureID + '_lastSection');
    //    $('#current_a').attr('href', currentChapterHref);
    //    $(this).hide();
    //    $('#current_a').show();
    //});
    
});
</script>
</body>
</html>
""")

outfile.close()
source.close()
