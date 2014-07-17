from flask import render_template


class mainView():
    def show(self):
        return render_template('MainView.html', name='test')

        
        
