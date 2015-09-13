from flask import redirect, url_for

# @auth.route('/logout')
def logout():
#     logout_user()
    return redirect(url_for('.login'))
