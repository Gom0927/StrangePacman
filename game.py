#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from player import Player
from enemies import *
import tkinter as tk
from tkinter import messagebox
import webbrowser

import random
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

class Game(object):
    def __init__(self):
        self.bicj = 0
        self.evolved = False

        self.font = pygame.font.Font('./Assets/PressStart2P-vaV7.ttf',40)
        self.about = False
        self.game_over = True
        self.win = False
        # Create the variable for the score
        self.score = 0
        # Create the font for displaying the score on the screen
        self.font = pygame.font.Font('./Assets/PressStart2P-vaV7.ttf',20)
        # Create the menu of the game
        self.menu = Menu(("Start","About","Exit"),font_color = WHITE,font_size=60)
        # Create the player
        self.player = Player(32,128,"./Assets/player.png")
        self.player_explosion = False
        # Create the blocks that will set the paths where the player can go
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # Create a group for the dots on the screen
        self.dots_group = pygame.sprite.Group()
        # Set the enviroment:
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
        # Create the enemies
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Slime(288,96,0,2))
        self.enemies.add(Slime(288,320,0,-2))
        self.enemies.add(Slime(544,128,0,2))
        self.enemies.add(Slime(32,224,0,2))
        self.enemies.add(Slime(160,64,2,0))
        self.enemies.add(Slime(448,64,-2,0))
        self.enemies.add(Slime(640,448,2,0))
        self.enemies.add(Slime(448,320,2,0))


        # Add the dots inside the game
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j*32+12,i*32+12,WHITE,8,8))

        # Load the sound effects
        self.pacman_sound = pygame.mixer.Sound("./Assets/pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("./Assets/game_over_sound.ogg")
        self.evolve_sound = pygame.mixer.Sound("./Assets/evolve.ogg")
        self.pass_attack_a_sound = pygame.mixer.Sound("./Assets/pass_attack_a.ogg")
        self.pass_attack_b_sound = pygame.mixer.Sound("./Assets/pass_attack_b.ogg")
        self.pass_attack_c_sound = pygame.mixer.Sound("./Assets/pass_attack_c.ogg")


    def process_events(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if self.score == 23:
                    if self.bicj == 4:
                        if self.evolved == False:
                            print('EVOLVE')
                            self.evolved = True
                            print(self.evolved)
                            self.evolve_sound.play()
                    else:
                        if keys[pygame.K_b]:
                            self.bicj += 1
                            print('B')
                            print(self.evolved)
                        if keys[pygame.K_i]:
                            self.bicj += 1
                            print('I')
                            print(self.evolved)
                        if keys[pygame.K_c]:
                            self.bicj += 1
                            print('C')
                            print(self.evolved)
                        if keys[pygame.K_j]:
                            self.bicj += 1
                            print('J')
                            print(self.evolved)

                if event.key == pygame.K_PAUSE:
                    messagebox.showinfo("UNBELIEVABLE", "How did you find this easter egg?????? mail to oconlygom@gmail.com")
                    self.game_end()

                if self.score >= 156:
                    self.game_end()

                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            # ---- START ------
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            # --- ABOUT ------
                            self.about = True
                        elif self.menu.state == 2:
                            # --- EXIT -------
                            # User clicked exit
                            return True

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()
                    
        return False

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks,self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player,self.dots_group,True)
            # When the block_hit_list contains one sprite that means that player hit a dot
            if len(block_hit_list) > 0:
                # Here will be the sound effect
                self.pacman_sound.play()
                self.score += 1
            block_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,True)
            if len(block_hit_list) > 0:
                print(self.evolved)
                if self.evolved == False:
                    print(self.evolved)
                    if self.player.explosion == False:
                        self.player.explosion = True
                        self.game_over_sound.play()
                        print('------------------------')
                elif self.evolved == True:
                    print(self.evolved)
                    num = random.randrange(0,4)
                    if num == 1:
                        self.pass_attack_a_sound.play()
                    elif num == 2:
                        self.pass_attack_b_sound.play()
                    elif num == 3:
                        self.pass_attack_c_sound.play()
                    else:
                        self.pass_attack_a_sound.play()
            self.game_over = self.player.game_over
            self.enemies.update(self.horizontal_blocks,self.vertical_blocks)

    def display_frame(self,screen):
        # First, clear the screen to white. Don't put other drawing commands
        screen.fill(BLACK)
        # --- Drawing code should go here
        if self.game_over:
            if self.about:
                label = self.font.render("BicJ Fan Game but not Fan", True, (255,255,255))
                label_ = self.font.render("BicJ Recorded Audio and Made by GomQ", True, (255,255,255))
                # Get the width and height of the label
                width = label.get_width()
                height = label.get_height()
                width_ = label_.get_width()
                height_ = label_.get_height()
                # Determine the position of the label
                posX = (SCREEN_WIDTH /2) - (width /2)
                posY = (SCREEN_HEIGHT /2) - (height /2)
                posX_ = (SCREEN_WIDTH /2) - (width_ / 2)
                posY_ = (SCREEN_HEIGHT /2) - (height_ * 2)
                # Draw the label onto the screen
                screen.blit(label,(posX,posY))
                screen.blit(label_,(posX_,posY_))
            else:
                self.menu.display_frame(screen)
        else:
            # --- Draw the game here ---
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image,self.player.rect)
            #text=self.font.render("Score: "+(str)(self.score), 1,self.RED)
            #screen.blit(text, (30, 650))
            # Render the text for the score
            text = self.font.render("Score: " + str(self.score),True,GREEN)
            # Put the text on the screen
            screen.blit(text,[120,20])
            
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def game_end(self):
        messagebox.showinfo("You Win!", "Thanks for playing BicJ Pacman")
        webbrowser.open_new("https://www.youtube.com/channel/UC_tOTO3zwPnayrUX-kQBrUw?sub_confirmation=1")
        webbrowser.open("https://twitch.tv/bicj0223")
        messagebox.showinfo("You Win!", "Subscribe and Follow BicJ")
        self.game_over = True
        self.score = 0


class Menu(object):
    state = 0
    def __init__(self,items,font_color=(0,0,0),select_color=(255,0,0),ttf_font='./Assets/PressStart2P-vaV7.ttf',font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        
    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item,True,self.select_color)
            else:
                label = self.font.render(item,True,self.font_color)
            
            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)
            # t_h: total height of text block
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height)
            
            screen.blit(label,(posX,posY))
        
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) -1:
                    self.state += 1
