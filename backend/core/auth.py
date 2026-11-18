from rest_framework.authentication import SessionAuthentication as Base


class SessionAuthentication(Base):
    def authenticate_header(self, request):
        return 'Session realm="EcoGest360"'
