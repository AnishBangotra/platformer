import pygame, json

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])) : 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])) : 1,
    tuple(sorted([(-1, 0), (0, 1)])) : 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])) : 3,
    tuple(sorted([(-1, 0), (0, -1)])) : 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])) : 5,
    tuple(sorted([(1, 0), (0, -1)])) : 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])) : 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])) : 8,
}

NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}
AUTOTILE_TYPES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        # for i in range(10):
            #horizontal line
            # self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            # #vertical line
            # self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}
            # self.tilemap['5;' + str(3 + i)] = {'type': 'grass', 'variant': 1, 'pos': (5, 3 + i)}
    
    def tiles_around(self, pos):
        tiles=[]
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1]) 
            if check_loc in self.tilemap:tiles.append(self.tilemap[check_loc])
        return tiles

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def physics_rects_around(self, pos):
        rects=[]
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                # Check if this loc type is same as our tile type 
                # If so, then we can consider it as neighbor
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            # Sorting our neighbors as per AUTOTILE Map structure
            neighbors = tuple(sorted(neighbors))
            # Updating the type of the tile by their neighbor variants
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]
        
    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # offset[0] // self.tile_size will give the top left tiles x position to the
        # last bottom right tile which we will get covering the display width and adding 1 for the last tile

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))