import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    """
    В ответе вся информация пользователя находится на корневом уровне,
    а не располагается в поле "user".
    Чтобы это исправить, нужно создать настраиваемое средство визуализации
    DRF (renderer).
    """
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # Если мы получим ключ token как часть ответа, это будет байтовый
        # объект. Байтовые объекты плохо сериализуются, поэтому нам нужно
        # декодировать их перед рендерингом объекта User.
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            # Декодируем token если он имеет тип bytes.
            data['token'] = token.decode('utf-8')

        # Отображаем наши данные в простанстве имен 'user'.
        return json.dumps({
            'user': data
        })