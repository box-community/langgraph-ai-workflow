from typing import TypedDict, Union

from pydantic import BaseModel, Field


StructuredResponseSchema = Union[dict, type[BaseModel]]


class BoxFileLocation(BaseModel):
    """Model for Box file location."""

    file_name: str = Field(None, description="Name of the file.")
    file_id: str = Field(None, description="Box file id.")
    parent_folder_name: str = Field(None, description="Name of the parent folder.")


class ScriptData(BaseModel):
    """Model for script data."""

    title: str = Field(None, description="Title of the script.")
    author: str = Field(None, description="Author of the script.")
    genre: str = Field(None, description="Genre of the script.")
    date: str = Field(None, description="Date of the script.")
    plot_summary: str = Field(None, description="Plot summary of the script.")


class Location(BaseModel):
    name: str = Field(None, description="Name of the location.")
    description: str = Field(None, description="Description of the location.")


class Locations(BaseModel):
    locations: list[Location] = Field(
        None, description="List of locations in the script."
    )


class SuggestedActor(BaseModel):
    name: str = Field(None, description="Name of the actor.")
    description: str = Field(None, description="Description of the actor.")


class Role(BaseModel):
    role: str = Field(None, description="Name of the movie role.")
    description: str = Field(None, description="Description of the role.")


class Roles(BaseModel):
    roles: list[Role] = Field(None, description="List of roles in the script.")


class Character(BaseModel):
    name: str = Field(None, description="Name of the character.")
    description: str = Field(None, description="Description of the character.")
    # role: str = Field(None, description="Role of the character.")
    suggested_actors: list[SuggestedActor] = Field(
        None, description="List of suggested actors for the character."
    )


class Characters(BaseModel):
    characters: list[Character] = Field(
        None, description="List of characters in the script."
    )


class Prop(BaseModel):
    name: str = Field(None, description="Name of the prop.")
    description: str = Field(None, description="Description of the prop.")


class Props(BaseModel):
    props: list[Prop] = Field(None, description="List of props in the script.")


class AuthorAccomplishment(BaseModel):
    name: str = Field(None, description="Name of the accomplishment.")
    description: str = Field(None, description="Description of the accomplishment.")


class AuthorOtherMovieScript(BaseModel):
    name: str = Field(None, description="Name of the other movie script.")
    description: str = Field(None, description="Description of the other movie script.")


class AuthorWorkedWith(BaseModel):
    name: str = Field(
        None, description="Name of the company or organizations worked with."
    )
    description: str = Field(
        None, description="Description of the company or organizations worked with."
    )


class Author(BaseModel):
    accomplishments: list[AuthorAccomplishment] = Field(
        None, description="List of accomplishments of the author."
    )
    other_movie_scripts: list[AuthorOtherMovieScript] = Field(
        None, description="List of other movie scripts by the author."
    )
    worked_with: list[AuthorWorkedWith] = Field(
        None, description="List of companies or organizations worked with the author."
    )


class Producer(BaseModel):
    name: str = Field(None, description="Name of the producer.")
    description: str = Field(
        None, description="Examples of work this producer is known for."
    )


class Producers(BaseModel):
    producers: list[Producer] = Field(
        None, description="List of producers for the script."
    )


class Director(BaseModel):
    name: str = Field(None, description="Name of the director.")
    description: str = Field(
        None, description="Examples of work this director is known for."
    )


class Directors(BaseModel):
    directors: list[Director] = Field(
        None, description="List of directors for the script."
    )


# Graph state
class WorkFlowState(TypedDict):
    box_script_file: BoxFileLocation
    script_file_read: str
    script_data: ScriptData
    locations: Locations
    roles: Roles
    characters: Characters
    props: Props
    author: Author
    producers: Producers
    directors: Directors
    markdown: str
