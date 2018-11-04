def gen_csv_for_video(video, celebrity):
    with open('results_%d.csv' % time.time(), 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        last_second = None
        celebrity_in_second = False
        for frame_file_name, second in video_frames_generator(video):
            if second != last_second:
                if last_second is not None:
                    print("%d , %d" % (last_second , int(celebrity_in_second)))
                    csvwriter.writerow([last_second, int(celebrity_in_second)])
                last_second = second
                celebrity_in_second = False

            with open(frame_file_name, mode='rb') as file:
                image = file.read()

            has_celebrity = is_celebrity_in_image(image, celebrity)
            celebrity_in_second = celebrity_in_second or has_celebrity
        if last_second != None:
            print("%d , %d" % (last_second , int(celebrity_in_second)))
            csvwriter.writerow([last_second, int(celebrity_in_second)])

def is_celebrity_in_image(image, celebrity):
    return bool(random.getrandbits(1))
            
def video_frames_generator(video):
    "Generates tuples (frame_file_name, second)"
    frame_filenames = [filename for filename in os.listdir(FRAMES_DIR) if is_frame_filename(filename)]
    frame_filenames.sort(key=normalize_frame_filename)

    for filename in frame_filenames:
        yield (FRAMES_DIR+filename, second_from_frame_number(normalize_frame_filename(filename)))

def normalize_frame_filename(filename):
    return int(filename[:-len('.bmp')])

def is_frame_filename(filename):
    p = re.compile('\d\.bmp')
    return p.search(filename)

