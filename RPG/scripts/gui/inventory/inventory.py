import pygame
from RPG.scripts.consts import INVENTORY_IMAGE, INVENTORY_CELL_IMAGE, INVENTORY_SELECTED_CELL_IMAGE, TILE_SIZE
from RPG.scripts.game_object import GameObject
from RPG.scripts.gui.inventory.cell import Cell
from RPG.scripts.gui.inventory.button import Button
from RPG.scripts.armor import Armor
from RPG.scripts.weapon import Weapon


class Inventory(GameObject):
    def __init__(self, game):
        super().__init__(game, INVENTORY_IMAGE, 0, 0, game.gui_group)
        self.rect.x = 1350
        self.rect.y = 200
        self.cells = []
        for i in range(45, 281, 95):
            for j in range(45, 376, 95):
                self.cells.append(Cell(self.game, self, 'cell', j, i))
        self.sword_slot = Cell(self.game, self, 'sword', 45, 645)
        self.bow_slot = Cell(self.game, self, 'bow', 140, 645)
        self.armor_slot = Cell(self.game, self, 'armor', 235, 645)
        self.ring_slot = Cell(self.game, self, 'ring', 330, 645)
        self.slots = [self.sword_slot, self.bow_slot, self.armor_slot, self.ring_slot]
        self.drop_btn = Button(game, self, 310, 465, 'drop')
        self.use_btn = Button(game, self, 310, 395, 'use')
        self.selected_cell = None

    def update(self):
        self.game.inventory_cell_group.draw(self.image)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                for cell in self.cells:
                    if cell.rect.collidepoint(event.pos):
                        if cell.item:
                            for i in range(len(self.cells)):
                                if self.cells[i].selected:
                                    self.cells[i].selected = False
                            for i in range(len(self.slots)):
                                if self.slots[i].selected:
                                    self.slots[i].selected = False
                            cell.selected = True
                            self.selected_cell = cell
                for slot in self.slots:
                    if slot.rect.collidepoint(event.pos):
                        if slot.item:
                            for i in range(len(self.cells)):
                                if self.cells[i].selected:
                                    self.cells[i].selected = False
                            for i in range(len(self.slots)):
                                if self.slots[i].selected:
                                    self.slots[i].selected = False
                            slot.selected = True
                            self.selected_cell = slot
                self.game.inventory_cell_group.update()
            if self.drop_btn.rect.collidepoint(event.pos):
                self.drop_item()
            if self.use_btn.rect.collidepoint(event.pos):
                if self.selected_cell:
                    self.selected_cell.item.use()
                    if isinstance(self.selected_cell.item, Armor):
                        print('a')
                    else:
                        for i in range(len(self.cells)):
                            if self.cells[i] == self.selected_cell:
                                self.cells[i].item = None
                                self.cells[i].selected = False
                                self.selected_cell = None
                    self.game.inventory_cell_group.update()

    def add_item(self, obj):
        for cell in self.cells:
            if not cell.item:
                cell.item = obj
                break
        self.game.inventory_cell_group.update()

    def drop_item(self):
        for i in range(len(self.cells)):
            if self.cells[i] == self.selected_cell:
                item = self.cells[i].item
                self.cells[i].item = None
                self.cells[i].selected = False
                self.selected_cell = None
                self.game.all_sprites.add(item)
                self.game.pickable_objects.add(item)
                item.x = self.game.player.x - 75
                item.y = self.game.player.y
                item.rect.x = self.game.player.rect.x - 75
                item.rect.y = self.game.player.rect.y
        for i in range(len(self.slots)):
            if self.slots[i] == self.selected_cell:
                item = self.slots[i].item
                if isinstance(item, Armor):
                    self.game.player.armor -= item.armor
                elif isinstance(item, Weapon):
                    if item.type == 'iron_sword':
                        self.game.player.damage -= item.damage
                    else:
                        self.game.player.bow_damage -= item.damage
                else:
                    item.remove_effect()
                self.slots[i].item = None
                self.slots[i].selected = False
                self.selected_cell = None
                self.game.all_sprites.add(item)
                self.game.pickable_objects.add(item)
                item.x = self.game.player.x - 75
                item.y = self.game.player.y
                item.rect.x = self.game.player.rect.x - 75
                item.rect.y = self.game.player.rect.y
        self.game.inventory_cell_group.update()

# TODO Доработать систему выкидывания вещей
