from extra_graphics import *
import pygame

class Button():
	def __init__(self, pos, text_input, font, base_color, hovering_color, bg_color = None, image = None):
		self.position = pos
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)

		self.background_color = bg_color
		self.image = image

		self.text_rect = self.text.get_rect(center=self.position)
		self.rect = self.text_rect.inflate(60,30)
		self.rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width - 8, self.rect.height - 9)

	def update(self, screen):
		if self.background_color is not None:
			draw_rect_alpha(screen, self.background_color, self.rect)
		if self.image is not None:
			screen.blit(self.image, self.image.get_rect(center=self.position))
			
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

class TextlessButton:
	def __init__(self, position: tuple[int, int], default_image, hover_image):
		self.position = position
		self.hover = False

		self.default_image =  default_image
		self.hover_image = hover_image

		self.default_rect = self.default_image.get_rect(center=self.position)
		self.hover_rect = self.hover_image.get_rect(center=self.position)

	def update(self, screen):
		if self.default_image is not None and self.hover == False:
			screen.blit(self.default_image, self.default_rect)
		elif self.hover_image is not None and self.hover == True:
			screen.blit(self.hover_image, self.hover_rect)

	def checkForInput(self, position):
		if position[0] in range(self.default_rect.left, self.default_rect.right) and position[1] in range(self.default_rect.top, self.default_rect.bottom) and self.hover == False:
			self.hover = True

		elif position[0] in range(self.hover_rect.left, self.hover_rect.right) and position[1] in range(self.hover_rect.top, self.hover_rect.bottom) and self.hover == True:
			self.hover = True
		else:
			self.hover = False


class ProgressBarWithSteps:
	def __init__(self, position: tuple[int, int], left_default, left_hover, right_default, right_hover, bar_color, default_value: int, min_value: int, max_value: int, width: int):
		self.position = position
		self.left_button = TextlessButton((position[0] - width // 2 + left_default.get_rect().width // 2, position[1]), left_default, left_hover)
		self.right_button = TextlessButton((position[0] + width // 2 - right_default.get_rect().width // 2, position[1]), right_default, right_hover)
		self.bar_color = bar_color
		
		self.width = width

		self.margin = 10

		self.bar_width = width - self.left_button.default_rect.width - self.right_button.default_rect.width - 2 * self.margin

		self.min_value = min_value
		self.max_value = max_value
		self.steps = self.max_value - self.min_value
		self.value = default_value

	def update(self, screen, position, pressed = False):
		self.left_button.checkForInput(position)
		self.right_button.checkForInput(position)

		self.left_button.update(screen)
		self.right_button.update(screen)

		if pressed:
			if self.left_button.hover:
				if self.value != self.min_value:
					return -1
			elif self.right_button.hover:
				if self.value != self.max_value:
					return 1
		return 0
	
	def draw(self, screen, value):
		self.value = value
		bar_rect = pygame.Rect(self.left_button.default_rect.right + self.margin, self.left_button.default_rect.top, self.bar_width / self.steps * self.value, self.left_button.default_rect.height)
		pygame.draw.rect(screen, self.bar_color, bar_rect)

class Price:
	def __init__(self, position, image, font, default_color, disabled_color='gray', insufficient_color='red', height=15):
		self.position = position
		self.font = font
		self.default_color = default_color
		self.disabled_color = disabled_color
		self.insufficient_color = insufficient_color
		self.height = height

		self.image = pygame.transform.scale_by(image, self.height / image.get_height())
		self.image_rect = self.image.get_rect(midleft = self.position)


	def draw(self, screen, text_str, state = "default"):
		if state == "disabled":
			color = self.disabled_color
		elif state == "insufficient":
			color = self.insufficient_color
		else:
			color = self.default_color

		if text_str.upper() == "MAX":
			text = self.font.render(text_str, True, color)
			text_rect = text.get_rect(midleft = self.position)
			screen.blit(text, text_rect)
		else:
			text = self.font.render(text_str, True, color)
			screen.blit(self.image, self.image_rect)
			text_rect = text.get_rect(topleft = (self.image_rect.right + 5, self.image_rect.top))
			screen.blit(text, text_rect)

