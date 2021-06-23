from TexSoup import TexSoup
import re 
import os
import shutil


class Fichier:
    def __init__(self, location):
        self.location = location
        self.working_dir = self.get_working_dir()
        self.filename = self.get_filename()

    def get_working_dir(self):
        return re.search(r'(\/[\w\s]+)+\/', self.location)[0] 

    def get_filename(self):
        return re.search(r'(?!<\/)[\w\.]+$', self.location)[0]

    def tex_cleancontent2str(self):
        # if self is a LaTeX document
        # return a string containing
        # \begin{document}
        # ...
        # \end{document}
        with open(self.location, 'r') as reader:
            data = reader.read()
        # remove header
        purifyinput = r'\\begin{document}(.|\n)*\\end{document}'
        match = re.search(purifyinput, data)
        data = match.group(0)

        # remove chapter and heading
        purifyinput = r'\\begin\{document\}\n(.|\n)*\\begin\{multicols\}\{2\}'
        data = re.sub(purifyinput, r'\\begin{document}\n\\begin{multicols}{2}', data)

        # remove any option from environments
        purifyinput = r'(\\begin\{\w*\})\[(.*)?\]'
        data = re.sub(purifyinput, r'\1', data)

        # replace \sitem by regular \items
        purifyinput = r'\\sitem'
        data = re.sub(purifyinput, r'\\item', data)

        # [ inside maths env aussi ?
        # c'est surtout le symbole [ qui fait tout planter
        right_bracket_inside_inline_env_re = r' \$[^\[\$]*\[[^\$]*\$'
        list_brackets = re.findall(right_bracket_inside_inline_env_re, data)
        for e in list_brackets:
            e_without_bracket = e.replace('[', '\\rb ')
            data = data.replace(e, e_without_bracket)

        # les $ s'y mettent ?
        inline_dollar_re = r'(?!<\$)\$'
        data = re.sub(inline_dollar_re, r' $ ', data)
        
        # les \left* \right* posent problème
        # doivent être précédés et succédés d'un espace
        purifyinput = r'\\left(.)'
        data = re.sub(purifyinput, r' \\left\1 ', data)
        purifyinput = r'\\right(.)'
        data = re.sub(purifyinput, r' \\right\1 ', data)

        # weird shananigans
        # purifyinput = r' \$([^\[\]\$]*)(?<!\\left)\[\s*([^;]*)\s*;\s*([^\]\$\[]*)\s*(?<!\\right)\]\s*\$'
        # data = re.sub(purifyinput, r'$\1 \\ffinterval{\2}{\3}$', data)
        # purifyinput = r' \$([^\[\]\$]*)(?<!\\left)\[\s*([^;]*)\s*;\s*([^\]\$\[]*)\s*(?<!\\right)\[\s*\$'
        # data = re.sub(purifyinput, r'$\1 \\fointerval{\2}{\3}$', data)
        # purifyinput = r' \$([^\[\]\$]*)(?<!\\left)\]\s*([^;]*)\s*;\s*([^\]\$\[]*)\s*(?<!\\right)\[\s*\$'
        # data = re.sub(purifyinput, r'$\1 \\oointerval{\2}{\3}$', data)

        return data

    def tex_extract_content_to_str(self):
        soup = TexSoup(self.tex_cleancontent2str())
        return [ str(e) for e in soup.enumerate.contents]

    def tex_extract_content_to_file(self, save_folder = None):
        if not save_folder:
            save_folder = self.working_dir +  "extracted_content/"
        try:
            shutils.rmtree(save_folder)
        except FileNotFoundError:
            os.mkdir(save_folder)

        get_items = self.tex_extract_content_to_str()
        for k in range(len(get_items)):
            exercice = get_items[k]
            # il reste le premier \item à nettoyer possiblement
            with open(save_folder + "{}.tex".format(k), "w") as output_file:
                output_file.write(str(exercice))


