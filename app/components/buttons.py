import streamlit as st


def home_button(label: str = "Home", route: str = "Home", width="content") -> None:
    """Create a button to navigate to the home page.

    Parameters
    ----------
    label : str, optional
        button label, by default "Home"
    route : str, optional
        route to navigate to, by default "Home"
    width : str, optional
        set the button width to the container width, by default content
    """
    st.button(
        label,
        type="secondary",
        on_click=to_home,
        args=(route,),
        width=width,
    )


def back_button(label: str = "Back", width="content") -> None:
    """Create a button to navigate back to the column selection page, keeping the imported data and selections.

    Parameters
    ----------
    label : str, optional
        button label, by default "Back"
    width : str, optional
        set the button width to the container width, by default content
    """
    st.button(
        label,
        type="secondary",
        on_click=to_column_selection,
        width=width,
    )


def to_home(route="Home"):
    """Navigate to the home page. If an error message is present, it is displayed.

    Parameters
    ----------
    route : str, optional
        route path, by default "Home"
    """
    error_message = None
    if "error" in st.session_state:
        error_message = st.session_state.error
    st.session_state.clear()
    if error_message:
        st.session_state.error = error_message
    st.session_state.page = route


def to_column_selection():
    """Navigate back to the column selection page. The imported dataframe, the selected columns and the selected algorithm
    are kept, while all algorithm specific state (e.g. the mining model and its parameters) is discarded.
    If no dataframe is available, the user is navigated to the home page instead.
    """
    if "df" not in st.session_state:
        to_home()
        return

    from app.config import algorithm_mappings

    df = st.session_state.df
    selected_columns = st.session_state.get("selected_columns", {})
    algorithm = st.session_state.get("algorithm")
    session_tmp_dir = st.session_state.get("session_tmp_dir")

    st.session_state.clear()

    st.session_state.df = df
    if session_tmp_dir is not None:
        st.session_state.session_tmp_dir = session_tmp_dir
    for column, value in selected_columns.items():
        st.session_state[column] = value
    for algorithm_name, algorithm_route in algorithm_mappings.items():
        if algorithm_route == algorithm:
            st.session_state.algorithm_selection = algorithm_name
            break
    st.session_state.page = "ColumnSelection"


def navigation_button(
    label: str,
    route: str,
    type="primary",
    width="content",
    beforeNavigate=None,
    args=None,
    disabled=False,
    key=None,
) -> None:
    """Create a button to navigate to a different page.

    Parameters
    ----------
    label : str
        button label
    route : str
        route to navigate to
    type : str, optional
        button type, by default "primary"
    width : str, optional
        set the button width to the container width, by default content
    beforeNavigate : function, optional
        function to execute before navigating, by default None
    args : tuple, optional
        arguments to pass to the beforeNavigate function, by default None
    disabled : bool, optional
        disable the button, by default False
    key : str, optional
        button key, by default None
    """
    if args is None:
        args = ()
    st.button(
        label,
        type=type,
        on_click=navigate_to,
        args=(route, beforeNavigate, *args),
        width=width,
        disabled=disabled,
        key=key,
    )


def navigate_to(route: str, beforeNavigate=None, *args):
    """Navigate to a different page.

    Parameters
    ----------
    route : str
        route to navigate to
    beforeNavigate : function, optional
        function to execute before navigating, by default None
    *args : tuple
        arguments to pass to the beforeNavigate function
    """
    st.session_state.page = route
    if beforeNavigate:
        beforeNavigate(*args)
