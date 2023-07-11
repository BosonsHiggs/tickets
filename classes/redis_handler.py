import json
import aioredis
import traceback

class RedisHandler:
	"""
	TODO: 
	exists: Verifica se uma chave existe no Redis.
	keys: Obtém todas as chaves que correspondem a um padrão especificado.
	incr: Incrementa o valor de uma chave numérica no Redis.
	decr: Decrementa o valor de uma chave numérica no Redis.
	expire: Define o tempo de expiração de uma chave no Redis.
	ttl: Obtém o tempo restante de expiração de uma chave no Redis.
	hset: Define um campo e um valor dentro de um hash no Redis.
	hget: Obtém o valor de um campo dentro de um hash no Redis.
	hdel: Remove um campo de um hash no Redis.
	hkeys: Obtém todas as chaves de campos dentro de um hash no Redis.
	hvals: Obtém todos os valores de campos dentro de um hash no Redis.
	hgetall: Obtém todos os campos e valores de um hash no Redis.
	"""
	def __init__(self, redis: aioredis.Redis):
		self.redis = redis

	async def save(self, key: str, data: dict):
		await self.redis.set(key, json.dumps(data))

	async def get(self, key: str):
		data = await self.redis.get(key)
		if data:
			return json.loads(data)
		else:
			return None

	async def delete(self, key: str):
		await self.redis.delete(key)

	async def exists(self, key: str):
		return await self.redis.exists(key)

	async def keys(self, pattern: str = '*'):
		return await self.redis.keys(pattern)

	async def incr(self, key: str, amount: int = 1):
		return await self.redis.incrby(key, amount)

	async def decr(self, key: str, amount: int = 1):
		return await self.redis.decrby(key, amount)

	async def expire(self, key: str, seconds: int):
		return await self.redis.expire(key, seconds)

	async def ttl(self, key: str):
		return await self.redis.ttl(key)

	async def hset(self, key: str, field: str, value: str):
		return await self.redis.hset(key, field, value)

	async def hget(self, key: str, field: str):
		return await self.redis.hget(key, field)

	async def hdel(self, key: str, field: str):
		return await self.redis.hdel(key, field)

	async def hkeys(self, key: str):
		return await self.redis.hkeys(key)

	async def hvals(self, key: str):
		return await self.redis.hvals(key)

	async def hgetall(self, key: str):
		return await self.redis.hgetall(key)
