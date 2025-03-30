<b>Для генерации приватного ключа</b>

<code>openssl genrsa -out jwt-private.pem 2048</code>

<b>Для генерации публичного ключа</b>

<code>openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem</code>