from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import gizeh

# load video 1
vid1 = VideoFileClip("video1.mp4")#.subclip(0, 4)
# vid1 = vid1.resize(0.7) # 70% of its size

# load video 2
vid2 = VideoFileClip("video2.mp4")#.subclip(0, 4)
vid2 = vid2.resize(height=vid1.h)



''' CREATE MASKS AND ADD IT TO VIDEOS '''

def create_circle(size, name):
    WIDTH, HEIGHT = size# vid1.size
    surface = gizeh.Surface(WIDTH, HEIGHT)

    circle = gizeh.circle(r=WIDTH//2, fill=(2,2,2), xy=(WIDTH//2, HEIGHT//2))
    circle.draw(surface)

    # save to png
    surface.write_to_png(name)

# generate mask png with correct size
create_circle(vid1.size, 'mask1.png')
create_circle(vid2.size, 'mask2.png')

''' FOR FIRST VIDEO '''
# load mask image
MASK_1 = ImageClip("mask1.png", transparent=True,ismask=True)
MASK_1 = MASK_1.set_duration(vid1.duration) # set duration
MASK_1 = MASK_1.set_fps(15) # set fps

# convert mask img to vido clip
MASK_1 = CompositeVideoClip([MASK_1], bg_color=(0),
                               size=vid1.size, ismask=True)
# set mask to video
vid1.mask = MASK_1 
vid1 = concatenate_videoclips([vid1], method='compose') # combine with video


# vid1.preview(audio=False)

''' FOR SECOND VIDEO '''
# load mask image
MASK_2 = ImageClip("mask2.png", transparent=True,ismask=True)
MASK_2 = MASK_2.set_duration(vid2.duration) # set duration
MASK_2 = MASK_2.set_fps(15) # set fps

# convert mask img to vido clip
MASK_2 = CompositeVideoClip([MASK_2], bg_color=(0),
                               size=vid2.size, ismask=True)
# set mask to video
vid2.mask = MASK_2 
vid2 = concatenate_videoclips([vid2], method='compose') # combine with video


# vid2.preview(audio=False)





''' ADD IMAGE TO THE VIDEO '''

image_clip1 =  ImageClip("image1.png", duration=vid1.duration)#.resize(0.5)
image_clip2 =  ImageClip("image2.png", duration=vid2.duration)#.resize(0.5)
image_clip2 = image_clip2.resize(height=image_clip1.h)


result1 = CompositeVideoClip([image_clip1, vid1.set_position(("right", "bottom")) ], use_bgclip=True)
result2 = CompositeVideoClip([image_clip2, vid2.set_position(("right", "bottom")) ], use_bgclip=True)


# add black area to left and right side
m = abs(image_clip1.w - image_clip2.w) 

if m%2 == 1: l,r = (m//2,m//2 + 1)
else: l,r = (m//2,m//2)

if image_clip1.w > image_clip2.w:
    result2 = result2.margin(left=l, right=r)
else:
    result1 = result1.margin(left=l, right=r)

print(result1.size, result2.size)
# result2 = result2.resize(result1.size) # just to be sure

# result2.preview(audio=False) 
# result2.ipython_display(width = 480)

# merge both the videos (vid1 and vid2 must be of same size/resolution before joining them)
final = concatenate_videoclips([result1, result2])


# final.preview(audio=False) 
final.write_videofile("output.mp4")





