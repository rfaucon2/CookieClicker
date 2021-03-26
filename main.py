import pygame as pg
pg.init()
pg.font.init()

class MainButton(pg.sprite.Sprite):
    def __init__(self, image, callback, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.cb = callback

    def callback(self):
        self.cb()

    def display(self, screen):
        screen.blit(self.image, self.rect)
        
    def getRect(self):
        return self.rect

class AutoClickerButton(pg.sprite.Sprite):
    def __init__(self, image, callback, x, y, price, strength, priceAugmentation):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.cb = callback
        self.price = price
        self.strength = 0
        self.baseStrength = strength
        self.priceAugmentation = priceAugmentation
        self.level = 0

    def callback(self):
        self.cb(self)

    def display(self, screen):
        screen.blit(self.image, self.rect)

    def getStrength(self):
        return self.strength

    def getPrice(self):
        return self.price

    def getLevel(self):
        return self.level

    def levelUp(self):
        self.level +=1
        self.strength = self.baseStrength * self.level
        self.price *= self.priceAugmentation

    def getRect(self):
        return self.rect

class App():
    def __init__(self):
        self.screenSize = [720, 480]
        self.screen = pg.display.set_mode(self.screenSize)
        self.background = pg.image.load("ressources/gradient.png")
        self.buttonList = []
        self.autoClickers = []
        self.lastLeftClickState = False
        self.cookieCounter = 0
        self.strength = 1
        self.autoStrength = 0
        self.tickCounter = 0
        self.initFont()
        self.initButtons()
        self.initButtonText()

    def initButtons(self):
        #Main button
        image = pg.image.load("ressources/cookie.png")
        self.mainButton = MainButton(image, self.upCookieCounter, (self.screenSize[0] / 2) - image.get_size()[0] / 2, (self.screenSize[1] / 2) - image.get_size()[1] / 2)
        self.buttonList.append(self.mainButton)

        #Basic auto clicker
        image = pg.image.load("ressources/upArrow.png")
        self.basicAutoClicker = AutoClickerButton(image, self.upAutoStrength, 100, 350, 100, 1, 1.5)
        self.buttonList.append(self.basicAutoClicker)
        self.autoClickers.append(self.basicAutoClicker)

        # Intermediate auto clicker
        image = pg.image.load("ressources/upArrow.png")
        self.intermediateAutoClicker = AutoClickerButton(image, self.upAutoStrength, 300, 350, 1000, 10, 1.85)
        self.buttonList.append(self.intermediateAutoClicker)
        self.autoClickers.append(self.intermediateAutoClicker)

        # Advanced auto clicker
        image = pg.image.load("ressources/upArrow.png")
        self.advencedAutoClicker = AutoClickerButton(image, self.upAutoStrength, 500, 350, 10000, 100, 2.5)
        self.buttonList.append(self.advencedAutoClicker)
        self.autoClickers.append(self.advencedAutoClicker)

    def initButtonText(self):
        self.basicAutoClickerText = [self.splatfont20.render("Auto clicker basique", True, [255, 255, 255]),
                                     self.splatfont20.render("Prix: " + str(self.basicAutoClicker.getPrice()), True, [255, 255, 255]),
                                     self.splatfont20.render("Puissance: " + str(self.basicAutoClicker.getStrength()), True, [255, 255, 255]),
                                     self.splatfont20.render("Niveau: " + str(self.basicAutoClicker.getLevel()), True, [255, 255, 255])]

        self.intermediateAutoClickerText = [self.splatfont20.render("Auto clicker intermediaire", True, [255, 255, 255]),
                                            self.splatfont20.render("Prix: " + str(self.intermediateAutoClicker.getPrice()), True,[255, 255, 255]),
                                            self.splatfont20.render("Puissance: " + str(self.intermediateAutoClicker.getStrength()),True, [255, 255, 255]),
                                            self.splatfont20.render("Niveau: " + str(self.intermediateAutoClicker.getLevel()), True,[255, 255, 255])]

        self.advancedAutoClickerText = [self.splatfont20.render("Auto clicker avancé", True, [255, 255, 255]),
                                     self.splatfont20.render("Prix: " + str(self.advencedAutoClicker.getPrice()), True,[255, 255, 255]),
                                     self.splatfont20.render("Puissance: " + str(self.advencedAutoClicker.getStrength()),True, [255, 255, 255]),
                                     self.splatfont20.render("Niveau: " + str(self.advencedAutoClicker.getLevel()), True,[255, 255, 255])]

    def initFont(self):
        self.splatfont20 = pg.font.SysFont("ressources/Splatfont.ttf", 20)
        self.splatfont30 = pg.font.SysFont("ressources/Splatfont.ttf", 30)
        self.cookieCounterText = self.splatfont30.render("Cookie: "+str(self.cookieCounter), True, [255, 255, 255])

    def upCookieCounter(self):
        self.cookieCounter += self.strength

    def upAutoStrength(self, button):
        if self.cookieCounter >= button.getPrice():
            self.cookieCounter -= button.getPrice()
            button.levelUp()
            autoStrength = 0
            for b in self.autoClickers:
                autoStrength += b.getStrength()
            self.autoStrength = autoStrength

    def run(self):
        while 1:
            #Check for all the events
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    quit()

                if pg.mouse.get_pressed()[0] == 1:
                    if not self.lastLeftClickState:
                        for b in self.buttonList:
                            if  (b.getRect().left <= pg.mouse.get_pos()[0] <= b.getRect().right) and (b.getRect().top <= pg.mouse.get_pos()[1] <= b.getRect().bottom):
                                b.callback()
                        self.lastLeftClickState = True
                else:
                    self.lastLeftClickState = False

            #Auto click every 500 ticks
            if self.tickCounter == 500:
                self.cookieCounter += self.autoStrength
                self.tickCounter = 0
            else:
                self.tickCounter += 1

            #Display the background
            self.screen.blit(self.background, (-50, -50))

            #Display all the buttons
            for b in self.buttonList:
                b.display(self.screen)

            #Upate and display all the button's textes
            self.basicAutoClickerText = [self.splatfont20.render("Auto clicker basique", True, [255, 255, 255]),
                                         self.splatfont20.render("Prix: " + str(self.basicAutoClicker.getPrice()), True,[255, 255, 255]),
                                         self.splatfont20.render("Puissance: " + str(self.basicAutoClicker.getStrength()), True,[255, 255, 255]),
                                         self.splatfont20.render("Niveau: " + str(self.basicAutoClicker.getLevel()),True, [255, 255, 255])]
            for i in range(1, 5):
                self.screen.blit(self.basicAutoClickerText[i-1], (self.basicAutoClicker.getRect()[0],
                                                             self.basicAutoClicker.getRect()[1] + self.basicAutoClicker.getRect().height + (i*10)+((i-1)*5)))

            self.intermediateAutoClickerText = [self.splatfont20.render("Auto clicker intermediaire", True, [255, 255, 255]),
                                                self.splatfont20.render("Prix: " + str(self.intermediateAutoClicker.getPrice()), True, [255, 255, 255]),
                                                self.splatfont20.render("Puissance: " + str(self.intermediateAutoClicker.getStrength()), True,[255, 255, 255]),
                                                self.splatfont20.render("Niveau: " + str(self.intermediateAutoClicker.getLevel()), True,[255, 255, 255])]
            for i in range(1, 5):
                self.screen.blit(self.intermediateAutoClickerText[i - 1], (self.intermediateAutoClicker.getRect()[0],
                                                                    self.intermediateAutoClicker.getRect()[1] + self.intermediateAutoClicker.getRect().height + (i * 10) + ((i - 1) * 5)))

            self.advancedAutoClickerText = [self.splatfont20.render("Auto clicker avancé", True, [255, 255, 255]),
                                            self.splatfont20.render("Prix: " + str(self.advencedAutoClicker.getPrice()),True, [255, 255, 255]),
                                            self.splatfont20.render("Puissance: " + str(self.advencedAutoClicker.getStrength()), True,[255, 255, 255]),
                                            self.splatfont20.render("Niveau: " + str(self.advencedAutoClicker.getLevel()), True,[255, 255, 255])]
            for i in range(1, 5):
                self.screen.blit(self.advancedAutoClickerText[i - 1], (self.advencedAutoClicker.getRect()[0],
                                                                    self.advencedAutoClicker.getRect()[1] + self.advencedAutoClicker.getRect().height + (i * 10) + ((i - 1) * 5)))

            #Update and display the score
            self.cookieCounterText = self.splatfont30.render("Cookie: "+str(self.cookieCounter), True, [255, 255, 255])
            self.screen.blit(self.cookieCounterText, (5, 5))

            #Update the screen
            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
