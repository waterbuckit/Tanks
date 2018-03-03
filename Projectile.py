class Projectile:
	def __init__(self, pos, vel, damage=0):
		self.pos = pos
		self.vel = vel
		self.damage = damage
	def getVel(self):
		return self.vel.getP()
	def update(self):
		self.pos += self.vel
	def draw(self, canvas):
		self.update()
		canvas.draw_circle(self.pos.getP(), 2, 1,'White', 'White')
