import time

from fire import Fire
import torch

from helpers import (
    get_character_to_search_for,
    get_window,
    mouse_click,
    take_screenshot_of_window,
    WINDOW_TYPE_HINT,
)


TOP_BORDER_PIXELS = 104  # not needed anymore, but I am too afraid to delete this line
BOTTOM_BORDER_PIXELS = 48


def main(
    yolo_object_detection_model_weights_path: str = '../runs/train/exp/weights/best.pt',
    verbose: bool = True,
) -> None:
    """
    Running the full logic needed to play the "Wanted!" minigame on a DeSmuME DS emulator.

    Once the game is loaded in the emulator, this function can be run in a terminal with:

    ```bash
    python run.py
    ```

    To override the default arguments, you can use the following syntax:

    ```bash
    python run.py --yolo_object_detection_model_weights=custom/path/to/weights.pt --verbose=False
    ```

    Parameters
    ----------
    yolo_object_detection_model_weights_path: str
        Path to the trained YOLOv5 object detection model weights file
    verbose: bool
        Whether or not to display print statements to the shell or not

    Notes
    -----
    Once this program is running, ensure that the DS emulator window is always at the forefront of
    the screen and remains fully visible. Do NOT resize the window or touch the mouse at all, except
    to kill the program run.

    """
    input(
        "*When you are happy with the window's position and ready to keep it in a single spot, "
        'press [Enter] to continue.*'
    )
    print('\n')

    # bookkeeping before we start the game loop
    yolo_object_detection_model = torch.hub.load(
        repo_or_dir='../02_train_detector/yolov5',
        model='custom',
        source='local',
        path=yolo_object_detection_model_weights_path,
        device='mps',
        verbose=verbose,
    )

    # making an assumption now that the window won't be moved at all once this is running - if i
    # is, then we have to move this logic inside the ``while`` loop, which is easy to do, just adds
    # some latency
    window = get_window(window_title='DeSmuME')

    dummy_image = take_screenshot_of_window(window=window)
    width, height = dummy_image.size

    window_width = window['kCGWindowBounds']['Width']
    window_height = window['kCGWindowBounds']['Height']
    image_width, image_height = dummy_image.size

    image_to_window_width_adjustment = window_width / image_width
    image_to_window_height_adjustment = window_height / image_height

    standard_bottom_half_screen_adjustment = (
        (window_height + (BOTTOM_BORDER_PIXELS * image_to_window_height_adjustment)) / 2
    )

    input(
        "\n\n*We are ready to go! When you're ready, reset the game and press [Enter] to play once "
        'you see the star!.*'
    )

    # dummy click on the window just to ensure it is active
    _click_with_relative_image_position(
        window=window,
        relative_x_adjustment=5,
        relative_y_adjustment=5,
    )

    time.sleep(0.1)

    # click the star
    _click_with_relative_image_position(
        window=window,
        relative_x_adjustment=((width / 2) * image_to_window_width_adjustment),
        relative_y_adjustment=(standard_bottom_half_screen_adjustment * 1.45),
    )

    time.sleep(8)

    # click the "Rec Room" button
    _click_with_relative_image_position(
        window=window,
        relative_x_adjustment=((width * 0.85) * image_to_window_width_adjustment),
        relative_y_adjustment=(standard_bottom_half_screen_adjustment * 1.8),
    )

    time.sleep(2.5)

    # click the "Wanted!" minigame
    _click_with_relative_image_position(
        window=window,
        relative_x_adjustment=((width * 0.345) * image_to_window_width_adjustment),
        relative_y_adjustment=(standard_bottom_half_screen_adjustment * 1.275),
    )

    time.sleep(4)
    from datetime import datetime
    while True:
        print('\n')

        image = take_screenshot_of_window(window=window)

        if verbose:
            print('Searching for a character to find...')

        print(datetime.now())
        character_to_find = get_character_to_search_for(image=image)
        print(datetime.now())

        if character_to_find is None:
            if verbose:
                print('No character detected yet!')

            # sleep a bit before trying the search again
            time.sleep(1)

            continue

        if verbose:
            print(f'Character to look for: {character_to_find}')

        while True:
            image = take_screenshot_of_window(window=window)

            cropped_image = image.crop(
                box=(
                    0,
                    int((height + BOTTOM_BORDER_PIXELS) / 2),
                    width,
                    height - BOTTOM_BORDER_PIXELS,
                ),
            )

            results = yolo_object_detection_model(cropped_image)

            results_pandas = results.pandas().xyxy[0]

            highest_confidence_boxes = results_pandas[results_pandas['name'] == character_to_find]

            if len(highest_confidence_boxes) > 0:
                highest_confidence_box = highest_confidence_boxes.iloc[0]
            else:
                if verbose:
                    print(f'{character_to_find} not yet found - will try again shortly!')

                time.sleep(0.5)
                continue

            if highest_confidence_box['confidence'] < 0.9:
                if verbose:
                    print(
                        'Bounding box confidence is not high enough to click - waiting a bit and '
                        'trying again soon.'
                    )

                time.sleep(0.5)
                continue

            x_mean = (highest_confidence_box['xmin'] + highest_confidence_box['xmax']) / 2
            y_mean = (highest_confidence_box['ymin'] + highest_confidence_box['ymax']) / 2

            _click_with_relative_image_position(
                window=window,
                # bounding box X-point multiplied by image-to-window width adjustment value from PIL
                # image to actual game window
                relative_x_adjustment=(x_mean * image_to_window_width_adjustment),
                relative_y_adjustment=(
                    # adjust window height to match the top of the cropped area from above
                    (
                        (window_height + (BOTTOM_BORDER_PIXELS * image_to_window_height_adjustment))
                        / 2
                    )
                    # bounding box Y-point multiplied by image-to-window height adjustment value
                    # from PIL image to actual game window
                    + (y_mean * image_to_window_height_adjustment)
                )
            )

            print('We clicked a character! Waiting a bit before doing it all over again!')

            time.sleep(4.5)

            break


def _click_with_relative_image_position(
    window: WINDOW_TYPE_HINT,
    relative_x_adjustment: float,
    relative_y_adjustment: float,
) -> None:
    """
    Move and click a spot on the screen relative to the top-left corner of the window ``window``.

    Parameters
    ----------
    window: dict (or an "Objective-C class __NSDictionaryI", to be specific)
        DS emulator window. Output of the function ``get_window``
    relative_x_adjustment: float
        Starting from the leftmost position in the window, how many additional pixels to move the
        mouse to the right before clicking
    relative_y_adjustment: float
        Starting from the topmost position in the window, how many additional pixels to move the
        mouse to the bottom before clicking

    """
    mouse_click(
        # window leftmost X-point + some adjustment amount towards the right
        x_position=window['kCGWindowBounds']['X'] + relative_x_adjustment,
        # window topmost Y-point + some adjustment amount towards the bottom
        y_position=window['kCGWindowBounds']['Y'] + relative_y_adjustment,
        click_delay=0.1,
    )


if __name__ == '__main__':
    Fire(main)
