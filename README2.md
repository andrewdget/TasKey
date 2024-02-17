
# TasKey - v0.0.0 (XX Feb, 2024)

[Report an Issue](https://github.com/andrewdget/TasKey/issues) | [View Changelog](https://github.com/andrewdget/TasKey/blob/main/CHANGELOG.md) | [Licensed under the MIT License](https://github.com/andrewdget/TasKey/blob/main/LICENSE.md)

## Create a New Task ```-n```
Creating a new task can be accomplished quickly by simply passing the ```-n``` leader flag followed by the desired task name, relying on TasKey's defaults to take care of the rest. For example:

```
TasKey >> -n Send Jim the new working directory.
```

However, if more control is required, the follower flags below can be 
used:

**Add a Footnote** ```-f```<br>Allows for the inclusion of additional information about/for the task and are always displayed, subtly, underneath the task name. Footnotes are optional, if no footnote is given for a task, none will be included. For example:

```
TasKey >> -n Send Jim the new working directory. -f Needs dir for Project_B along with permissions.
```

>[!TIP]
>Keep task names concise. If necessary, use footnotes to capture more nuanced information. 

**Set Task Priority** ```-l``` (low), ```-m``` (medium), ```-h``` (high), ```-c``` (critical)<br>The priority of a task influences how quickly that task will be at the top of the task list. Naturally, tasks with higher priority will be listed above other tasks with the same deadline/number of working days remaining. Furthermore, if a deadline is not manually set, the priority of the task influences the deadline that is automatically set (i.e. how many working days are provided to complete the task), see [Theory of Operation](url) for more. If no priority is set, TasKey will set the task to a medium priority. For example, creating a high priority task:

```
TasKey >> -n Send Jim the new working directory. -h 
```

**Set Task Deadline** ```-d```<br>A task's deadline (specifically, the number of working days remaining before the deadline), along with that task's level of priority, influence how quickly that task will be at the top of the task list. All TasKey tasks are assigned a deadline at creation, if not done manually (given in mmddyyyy format), a deadline will be automatically set based on priority, see [Theory of Operation](url) for more. For example, setting a deadline of February 18 2024:

```
TasKey >> -n Send Jim the the new working directory. -d 02182024
```

## Edit an Existing Task ```-e```

Editing a task works much the same as creating one, with all the same flag/attribute pairs, with two exceptions; the necessity of including an [alpha index](url) which points to the task to be edited, and the addition of the ```-n``` flag used to edit the tasks name.

When making adjustments to a task, only the flag(s) for the specific element(s) you wish to edit (i.e. the name, footnote, priority, or deadline) need to be called, all other elements will be inherited from the original task. 

**Edit Task Name** ```-n```<br>The attribute (task name string) provided will completely replace the original task name. For example, editing the name of a task at alpha index ```ab```:

```
TasKey >> -e ab -n Send Carla the the new working directory.
```

**Edit Task Footnote** ```-f```<br>The attribute (footnote string) provided will completely replace the original footnote. For example, editing the footnote of a task at alpha index ```ab```:

```
TasKey >> -e ab -f Needs dir for Project_C along with permissions.
```

>[!TIP]
>In order to remove a footnote from a task all together, simply pass ```None``` as the attribute.

**Edit Task Priority** ```-l``` (low), ```-m``` (medium), ```-h``` (high), ```-c``` (critical)<br>When a tasks priority is edited the deadline for that task (if it was not manually set) will be adjusted accordingly, see [Theory of Operation](url). However, the number of working days provided to complete the task remains relative to the original creation date (i.e. the deadline is re-set as if the task was given the new priority, when the task was originally created). For example, changing the priority of a task at alpha index ```ab``` to critical:

```
TasKey >> -e ab -c
```

**Edit Task Deadline** ```-d```<br>The attribute (task deadline - given in mmddyyyy format) provided will completely replace the original. For example, changing the deadline of a task at alpha index ```ab``` to March 18 2024:

```
TasKey >> -e ab -d 03182024
```

>[!TIP]
>In order to remove a manually set deadline, simply pass ```None``` as the attribute and a deadline will be set automatically according to the tasks priority (see [Theory of Operation](url)).

## Completing a Task ```-c```

When a task has been completed, it can be marked as such and subsequently moved from the main database to the archive database. This is acomplished by simply passing the ```-c``` flag along with the alpha index pointing to the target task. For example, marking a task complete at alpha index ```ab```:

```
TasKey >> -c ab
```

## Deleting a Task ```-d```

When necesary tasks can be deleted by simply passing the ```-d``` flag along with the alpha index pointing to the target task. The behavior of the delete command is context specific. If used within the main view, the task will be moved from the main database to the archive database. If used within the archive view, the task will be permanently delted from all databases. For example, deleting a task at alpha index ```ab```:

```
TasKey >> -d ab
```

## Restore a Completed/Deleted Task ```-r```

If a task has been completed or deleted in error, it can be restored (from the [archvie view](url)) by uising the ```-f``` flag along with the alpha index pointing to the target task. For example, restoring a task at alpha index ```ab```:

```
TasKey >> -r ab
``` 

## View Task Information ```-i```

All elements/information about a task can be displayed by passing the ```-i``` flag and the alpha index pointing to the target task. This will open a file-tree like drop down containing the additional information. For example, displaying additional information for a task at alpha index ```ab```:

```
TasKey >> -i ab
```

When done, the additional information can be hidden but using the same ```-i``` flag can be passeed but with ```None``` as the attribute.

## Switching to Archive View ```-a```

When an active task is completed or delted, it is moved from the active ("main") database to the archvie database. This database can be viewed by using the ```-a``` standalone flag. From the archive view, information about completed/deleted tasks can be viewed or restored.

## Returning to Main View ```-m```

In order to return to the active ("main") database view from the archive view, the standalone flag ```-m``` can be passed.

## Switch Tabs ```-t```

TasKey can support multiple task databases (such as one for a current project, another for personal tasks, etc.). These databases are organized into "tabs" which can be switched between at will, using the ```-t``` flag with the name of the tab as an attribute (Note, the tab name is case-sensitive). For example, switching to a tab/task database called "Project_C":

```
TasKey >> -t Project_C
```

## Generate Savestate ```-s```

## Clean Up/Prune Savestates ```-p```

## Close/Kill Application ```-k```

## Command Quick Reference

### Create a new Task

| Flag | Action | Attribute | Default Behavior |
| --- | --- | --- | --- |
| ```-n``` [Leader] | Create New Task | Task Name String | ~ |
| ```-f``` | Add a Footnote | Footnote String | ```None``` |
| ```-l```, ```-m```, ```-h```, ```-c``` | Set Task Priority (respectively; low, medium, high, critical) | None | ```-m``` |
| ```-d``` | Set Task Deadline| Deadline (mmddyyyy) | Dynamically Set[^1] |

### Edit an Existing Task

| Flag | Action | Attribute |
| --- | --- | --- |
| ```-e``` [Leader] | Edit an Existing Task | Target Alpha Index |
| ```-n``` | Edit Task | Task Name (string) |
| ```-f``` | Edit Task Footnote | Footnote (string) |
| ```-l```, ```-m```, ```-h```, ```-c``` | Edit Task Priority (respectively; low, medium, high, critical) | None |
| ```-d``` | Edit Task Deadline | Deadline (mmddyyyy) |

### Other Commands

| Flag | Action | Attribute |
| --- | --- | --- |
| ```-c``` | Complete a Task | Target Alpha Index |
| ```-d``` | Delete a Task[^2] | Target Alpha Index |
| ```-r``` | Restore a Completed/Deleted Task | Target Alpha Index |
| ```-i``` | View Task Information | Target Alpha Index |
| ```-a``` | Switch to Archive Database View | None |
| ```-m``` | Switch to Main Database View | None |
| ```-t``` | Switch Tabs | Tab Name |
| ```-s``` | Save Task Database | None |
| ```-p``` | Clean Up ("prune") Old Database Savestates | None |
| ```-k``` | Close ("kill") Application | None |

[^1]: See [Theory of Operation](url). 
[^2]: Behavior of delete command is context specific. See [Delete a Task](url).
