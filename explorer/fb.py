__author__ = 'sasinda'
import facebook

api_version = 'v2.5'
app_id='1026357457425742'
app_secret='62c89e23affe41bc9fab74b3485ad070'
app_token='1026357457425742|3ivOpHQj1Hx0Hn66pCU0LtOy_c8'
user_token_dev='CAAOld3eplU4BAIVNfHRMb7Vwa9hi92kqdJyRcHpFl74hvVMLZBtC62Ws7f4kL7bxxZCuUhPiRZBBxpbwzpZBUHk8LAnLBwjYGWFV6ehSBCX7rfiTwu8nbVXiT7B3SSasABZBuFkZAiyTaGNj1bv74m4x57KXczQmZBlaBgAJuAiwjKQkd3qXz1ZAgDpuSEoB8ZCjb6X5S00GpJAZDZD'

graph = facebook.GraphAPI(access_token=user_token_dev)
profile = graph.get_object('me')
friends=graph.get_connections(id='me', connection_name='friends')
# feed=graph.get_connections(id='me', connection_name='feed')
posts=graph.get_connections(id='me', connection_name='posts')

#Donald trump posts
posts=graph.get_connections(id='DonaldTrump', connection_name='posts')
