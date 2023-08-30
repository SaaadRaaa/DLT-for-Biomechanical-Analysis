import cv2
import numpy as np

# Marker detection parameters
font = cv2.FONT_HERSHEY_SIMPLEX  # Font for the marker numbers
font_scale = 0.7  # Font scale for the marker numbers
font_thickness = 2  # Font thickness for the marker numbers


def returnUV(video_paths, marker_threshold=60, minArea=20):
    # Initialize the list to store marker coordinates
    uv = []

    # Process each video
    for video_path in video_paths:
        # Initialize the video capture
        video = cv2.VideoCapture(video_path)

        # Get the total number of frames in the video
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # List to store the marker coordinates for the current video
        video_markers = []

        # Flag to indicate if ID assignment is in progress
        assigning_ids = True

        def assign_marker_id(event, x, y, flags, param):
            if assigning_ids and event == cv2.EVENT_LBUTTONDOWN:
                marker_id = len(video_markers) + 1
                video_markers.append((x, y))
                cv2.putText(frame, str(marker_id), (x, y - 10), font,
                            font_scale, (0, 0, 255), font_thickness)
                cv2.imshow("Marker Detection", frame)

        # Create a window for displaying the video
        cv2.namedWindow("Marker Detection", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Marker Detection", assign_marker_id)

        frame_count = 0  # Counter to keep track of frame number

        while True:
            # Capture a frame from the video
            ret, frame = video.read()

            if not ret:
                break

            # Increment frame counter
            frame_count += 1

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to isolate the markers
            _, thresholded = cv2.threshold(
                gray, marker_threshold, 255, cv2.THRESH_BINARY)

            # Find contours of the markers
            contours, _ = cv2.findContours(
                thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Update the marker positions in the current frame
            for contour in contours:
                # Calculate the contour area to filter out small detections
                area = cv2.contourArea(contour)

                if area > minArea:  # Adjust the minimum area threshold based on marker size
                    # Get the bounding box of the contour
                    x, y, w, h = cv2.boundingRect(contour)

                    # Calculate the centroid of the marker
                    cx = x + (w // 2)
                    cy = y + (h // 2)

                    # Draw a rectangle around the marker (in red color)
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 0, 255), 2)

                    # Put a question mark on the marker
                    cv2.putText(frame, "?", (x, y - 10), font,
                                font_scale, (0, 0, 255), font_thickness)

            # Display the frame with the detected markers
            cv2.imshow("Marker Detection", frame)

            # Stop the video and wait for user input to assign IDs
            if assigning_ids:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    assigning_ids = False
                    cv2.destroyAllWindows()

        # Reopen the video capture for marker tracking
        video.release()
        video = cv2.VideoCapture(video_path)

        # Read the first frame for marker tracking
        ret, prev_frame = video.read()

        # Convert the first frame to grayscale
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        frame_count = 0  # Reset frame counter

        while True:
            # Capture a frame from the video
            ret, frame = video.read()

            if not ret:
                break

            # Increment frame counter
            frame_count += 1

            # Convert the current frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Track the markers using Lucas-Kanade optical flow
            if len(video_markers) > 0:
                prev_points = np.array(
                    video_markers, dtype=np.float32).reshape(-1, 1, 2)
                curr_points, status, _ = cv2.calcOpticalFlowPyrLK(
                    prev_gray, gray, prev_points, None)

                # Update the marker positions based on the optical flow result
                video_markers = curr_points.reshape(-1, 2).tolist()
            else:
                # No previously detected markers, use the initial detection for the first frame
                video_markers = []

            # Draw the markers with assigned IDs
            for marker_id, position in enumerate(video_markers, start=1):
                cx, cy = position

                # Draw the marker with the assigned ID
                cv2.putText(frame, str(marker_id), (int(cx), int(cy) - 10), font,
                            font_scale, (0, 0, 255), font_thickness)

            # Display the frame with the tracked markers
            cv2.namedWindow("Marker Tracking", cv2.WINDOW_NORMAL)
            cv2.imshow("Marker Tracking", frame)

            # Append the marker coordinates to the current frame in the uv list
            if frame_count <= len(uv):
                uv[frame_count - 1].append(video_markers.copy())
            else:
                uv.append([video_markers.copy()])

            # Update the previous frame and previous points for the next iteration
            prev_gray = gray.copy()

            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture and close the window
        video.release()
        cv2.destroyAllWindows()

    return uv
