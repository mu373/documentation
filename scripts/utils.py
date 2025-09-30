from matplotlib.colors import ListedColormap

colors_cbfp = [
    [
        "#999999",
        "#E69F00",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#0072B2",
        "#D55E00",
        "#CC79A7",
    ],
    [
        "#000000",
        "#E69F00",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#0072B2",
        "#D55E00",
        "#CC79A7",
    ],
]

cmap_cbfp1 = ListedColormap(colors_cbfp[0])
cmap_cbfp2 = ListedColormap(colors_cbfp[1])


def get_cbfp_colors(n):
    if n == 1:
        return colors_cbfp[0]
    elif n == 2:
        return colors_cbfp[1]
    else:
        raise ValueError("Invalid CBFP color palette number.")


def get_cbfp_cmap(n):
    if n == 1:
        return cmap_cbfp1
    elif n == 2:
        return cmap_cbfp2
    else:
        raise ValueError("Invalid CBFP color palette number.")


def show_animation_video_base64(
    ani,
    dpi=200,
    type="mp4",
    autoplay=True,
    control=True,
    loop=True,
    fps=20,
    retina=True,
):
    """
    Display the animation as an MP4 video in Jupyter Notebook using base64 embedding.

    Parameters:
    ani : FuncAnimation
        The animation object to display.
    dpi : int
        Dots per inch for the saved video. Default is 200.

    Returns:
    None
    """
    from IPython.display import HTML, display
    import base64
    import tempfile

    suffix_dict = {"mp4": ".mp4", "webm": ".webm"}
    mimetype_dict = {"mp4": "video/mp4", "webm": "video/webm"}

    # Create a temporary file with .mp4 extension
    with tempfile.NamedTemporaryFile(suffix=suffix_dict[type], delete=False) as tmpfile:
        tmp_path = tmpfile.name

    # Save the animation to the temporary file using the 'ffmpeg' writer
    ani.save(tmp_path, writer="ffmpeg", fps=fps, dpi=dpi)

    # Read the video file and encode it in base64
    with open(tmp_path, "rb") as f:
        video_data = f.read()
        b64 = base64.b64encode(video_data).decode("utf-8")

    video_tag_options = ""
    if autoplay:
        video_tag_options += "autoplay muted "
    if control:
        video_tag_options += "controls "
    if loop:
        video_tag_options += "loop "

    classNames = ""
    if retina:
        classNames += "retina"

    # Create HTML to embed the video with controls
    html = f'''
    <video playsinline {video_tag_options} class="{classNames}">
      <source src="data:{mimetype_dict[type]};base64,{b64}" type="{mimetype_dict[type]}">
    </video>
    '''
    display(HTML(html))


def show_fig_svg(fig):
    import io
    from IPython.display import SVG, display

    # Save the figure into a string buffer as SVG
    buf = io.StringIO()
    fig.savefig(buf, format="svg")
    buf.seek(0)

    # Display the SVG image
    display(SVG(buf.getvalue()))
