import streamlit as st


class AppSession:
    keys = ["user_id", "role", "access_token", "refresh_token"]

    @classmethod
    def clear(cls) -> None:
        for key in cls.keys:
            st.session_state[key] = None

    @classmethod
    def is_initialized(cls) -> bool:
        return all(key in st.session_state for key in cls.keys)

    @classmethod
    def is_authenticated(cls) -> bool:
        return all(st.session_state.get(key) is not None for key in cls.keys)
