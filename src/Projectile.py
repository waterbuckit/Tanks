import math
class Projectile:
	def __init__(self, pos, vel, speed, rng=500, rad=3, damage=0):
		self.pos = pos
		self.vel = vel * speed # Multiplying normalized vel by scalar to implement varying projectile speeds
		self.damage = damage
		self.rad = rad
		self.range = rng
		self.travelled = 0
	def getVel(self):
		return self.vel.getP()
	def isWithinRange(self):
		return self.travelled < self.range
	def update(self):
		hyp = math.sqrt(abs(self.vel.x**2) + abs(self.vel.y**2))
		self.travelled += hyp
		self.rad -= self.rad / (self.range / hyp)
		self.pos += self.vel
	def draw(self, canvas):
		self.update()
		canvas.draw_circle(self.pos.getP(), self.rad, 1,'White', 'White')
