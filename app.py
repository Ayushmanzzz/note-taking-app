import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("📕Note Manager")  


#Create note
with st.expander("➕ Create New Note", expanded=True):
    title = st.text_input("Title")
    content = st.text_area("Content")
    tags = st.text_input("Tags(__ , __ , ..)")

    if st.button("Create Note"):
        if not title or not content:
            st.error("Title and Content are required")
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        res = requests.post(
            f"{BASE_URL}/notes/", 
            json={"title": title, "content": content, "tags": tag_list})
        
        if res.status_code in [200, 201]:
            st.success("Note Created Successfully")
        else:
            st.error(f"Error:{res.text}")
    
#view all notes
st.header("📋 All Notes")
if st.button("🔄 Refresh Notes"):
    st.session_state["refresh"] = True

if "refresh" not in st.session_state:
    st.session_state["refresh"] = True

if st.session_state["refresh"]:
    res = requests.get(f"{BASE_URL}/notes/")

    if res.status_code == 200:
        notes = res.json()

        for note in notes:
            st.subheader(note["title"])
            st.write(note["content"])

            if note["tags"]:
                st.caption("Tags: " + ", ".join(note["tags"]))

                col1, col2 = st.columns(2)

    #Delete note
                with col1:
                    if st.button(f"Delete {note['id']}", key = f"del_{note['id']}"):
                        d = requests.delete(f"{BASE_URL}/notes/{note['id']}")
                        if d.status_code == 200:
                            st.success("Note Deleted.")
                        else:
                            st.error("Delete Failed.")

    #Update Note
                with col2:
                    with st.expander(f"Update {note['id']}"):
                        new_title = st.text_input("New Title", key=f"title_{note['id']}")
                        new_content = st.text_area("New Content", key=f"content_{note['id']}")
                        new_tags = st.text_input("New Tags", key=f"tags_{note['id']}")

                    if st.button("Update", key=f"update_{note['id']}"):
                        updated_tags = [t.strip() for t in new_tags.split(",") if t.strip()]

                        u = requests.put(f"{BASE_URL}/notes/{note['id']}",
                                        json={
                                            "title": new_title or note["title"],
                                                "content": new_content or note["content"],
                                                "tags": updated_tags or note["tags"]
                                        })
                        
                        if u.status_code == 200:
                            st.success("Note Updated.")
                        else:
                            st.error("Update failed.")

                st.divider()
            
            else:
                st.error("Failed to fetch notes")