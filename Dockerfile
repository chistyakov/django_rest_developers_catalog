FROM python:3.6

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

ENV HOST=0.0.0.0
ENV PORT=8000
ENV SECRET_KEY='s29-f=*#v_u^n)u^x08cgiq(_x2_(cunb-xsnnm7%+z!ijo8@g'
ENV DEBUG=1
ENV SUPERUSERNAME=admin
ENV SUPERUSEREMAIL=al.ol.chistyakov@gmail.com
ENV SUPERUSERPASSWORD=password

WORKDIR saprun_tasks

RUN python3 manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('$SUPERUSERNAME', '$SUPERUSEREMAIL', '$SUPERUSERPASSWORD')" | python manage.py shell
CMD python3 manage.py runserver $HOST:$PORT