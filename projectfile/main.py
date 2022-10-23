from website import create_app

if __name__=='__main__':
    napp=create_app()
    napp.run(debug=True)


from flask import Blueprint,render_template, redirect, url_for, request, flash

#Handling error 404 and displaying relevant web page
@napp.errorhandler(404)
def internal_error(error):
    return render_template('<h3>error</h3>')