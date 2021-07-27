import matplotlib.pyplot as plt
from matplotlib import patches
import streamlit as st

class FloorPlan:

    def __init__(self, room_width, room_length, panel_width, panel_length, minimum_width):
        self.room_width = room_width * 1000
        self.room_length = room_length * 1000
        
        self.panel_width = panel_width
        self.panel_length = panel_length

        self.minimum_width = minimum_width

        self.tiling_plan = []

        self.tiles_used = 0


        self.current_size = self.panel_width
        self.remaining_size = 0
        self.width_covered = 0

        self.ended_in_else = False


    def tile(self):

        for i in range(int(self.room_length/self.panel_length)):
            self.tiling_plan.append([])
            tiles_used = 0
            while self.width_covered != self.room_width:
                
                if self.current_size <= self.room_width - self.width_covered:
                    if self.current_size < self.minimum_width:
                        self.current_size = self.panel_width
                        tiles_used += 1
                    tiles_used += 1
                    self.tiling_plan[-1].append(self.current_size)
                    self.width_covered += self.current_size
                    self.current_size = self.panel_width

                    self.ended_in_else = False

                else:
                    new_size = self.room_width - self.width_covered
                    if new_size < self.minimum_width:
                        self.current_size = self.tiling_plan[-1][0]
                        self.tiling_plan[-1].clear()
                        self.width_covered = 0
                        tiles_used = 0
                        self.current_size -= self.minimum_width - new_size
                        continue

                    self.remaining_size = self.current_size - new_size 

                    self.current_size = new_size
                    self.tiling_plan[-1].append(self.current_size)
                    self.width_covered += self.current_size

                    self.current_size = self.remaining_size

                    self.ended_in_else = True
            self.tiles_used += tiles_used
            self.width_covered = 0
        
        if self.ended_in_else:
            self.tiles_used += 1

        #print("Tiles used:", self.tiles_used)
        #print("Tiling Plan:")
        
        fig = plt.figure(figsize=(20, 15))
        ax = fig.add_subplot(111, aspect='equal')
        
        y = 0
        line = 1
        for i in self.tiling_plan:
            st.write(line, i)
            line += 1
        
        self.tiling_plan.reverse()
        for i in self.tiling_plan:
            x = 0
            for j in i:

                plt.axis([0, self.room_width,0, self.room_length])
                ax.add_patch(
                    patches.Rectangle(
                        (x, y),  # (x,y)
                        j,          # width
                        self.panel_length, # height
                        facecolor = "#00ffff",
                        edgecolor = "black",
                        linewidth = 1
                    )
                )
                x += j
            y += self.panel_length
        st.write(fig)
        fig.savefig("output.png", dpi=144) 
        return self.tiles_used
        


room_w = st.text_input("Enter Room Width (in meters):", "2.1")
room_l = st.text_input("Enter Room Length (in meters):", "0.8")
panel_w = st.text_input("Enter Panel Width (in milimeters):", "1300")
panel_l = st.text_input("Enter Panel Length (in milimeters):", "100")
min_w = st.text_input("Enter Minimum Width (in milimeters):", "150")

if st.button('Tile Floor!'):
    room_width = float(room_w)
    room_length = float(room_l)
    panel_width = float(panel_w)
    panel_length = float(panel_l)
    minimum_width = float(min_w)


    F = FloorPlan(room_width, room_length, panel_width, panel_length, minimum_width)
    used = F.tile()

    st.write("Total Tiles Used = " + str(used))
