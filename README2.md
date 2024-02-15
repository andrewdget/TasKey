
## Creating a New Task ```-n```

Creating a new task can be accomplished quickly by simply passing the ```-n``` leader flag followed by the desired task name, relying on TasKey's defaults to take care of the rest. For example:

```
TasKey >> -n Send Jim the new working directory.
```

However, if more control is required, the follower flags below can be used:

**Add a Footnote** ```-f```<br>Allows for the inclusion of additional information about/for the task and are always displayed, subtly, underneath the task name. Footnotes are optional, if no footnote is given for a task, none will be included. For example:

```
TasKey >> -n Send Jim the new working directory. -f Needs dir for Project_B along with permissions.
```

>[!TIP]
> Keep task names concise. If necessary, use footnotes to capture more nuanced information. 

**Set Task Priority** ```-l``` (low), ```-m``` (medium), ```-h``` (high), ```-c``` (critical)<br>The priority of a task influences how quickly that task will be at the top of the task list. Naturally, tasks with higher priority will be listed above other tasks with the same deadline/number of working days remaining. Furthermore, if a deadline is not manually set, the priority of the task influences the deadline that is automatically set (i.e. how many working days are provided to complete the task), see [Theory of Operation](url) for more. If no priority is set, TasKey will set the task to a medium priority. For example, creating a high priority task:

```
TasKey >> -n Send Jim the new working directory. -h 
```

**Set Task Deadline** ```-d```<br>A task's deadline (specifically, the number of working days remaining before the deadline), along with that task's level of priority, influence how quickly that task will be at the top of the task list. All TasKey tasks are assigned a deadline at creation, if not done manually (given in mmddyyyy format), a deadline will be automatically set based on priority, see [Theory of Operation](url) for more. For example, setting a deadline of February 18 2024:

```
TasKey >> -n Send Jim the the new working directory. -d 02182024
```

## Editing an Existing Task ```-e```

Task inherits all non-edits components from original task. 

## Completing a Task ```-c```
## Deleting a Task ```-d```

Behavior of delete command is context specific: If in main view, task will be moved to archive as a deleted task. If in archive view, task will be permanently deleted from database. 


## View Task Information ```-i```
## Switching to Archive View ```-a```
## Returning to Main View ```-m```
## Switch Tabs ```-t```
## Generate Savestate ```-s```
## Clean Up/Prune Savestates ```-p```
## Close/Kill Application ```-k```

## Command Quick Reference

### Creating a new Task

| Flag | Action | Attribute | Default Behavior |
| --- | --- | --- | --- |
| ```-n``` [Leader] | Create a new task. | Task Name String | ~ |
| ```-f``` | Add a footnote to task. | Footnote String | ```None``` |
| ```-l```, ```-m```, ```-h```, ```-c``` | Set task priority (respectively; low, medium, high, critical). | None | ```-m``` |
| ```-d``` | Set task deadline. | Deadline (mmddyyyy) | Dynamically Set[^1] |

### Editing an Existing Task

| Flag | Action | Attribute |
| --- | --- | --- |
| ```-e``` [Leader] | Edit existing task. | Target Alpha Index |
| ```-n``` | Edit task name. | Task Name (string) |
| ```-f``` | Edit task footnote. | Footnote (string) |
| ```-l```, ```-m```, ```-h```, ```-c``` | Edit task priority (respectively; low, medium, high, critical). | None |
| ```-d``` | Edit task deadline. | Deadline (mmddyyyy) |

### Other Commands

| Flag | Action | Attribute |
| --- | --- | --- |
| ```-c``` | Complete a task. | Target Alpha Index |
| ```-d``` | Delete a task.[^2] | Target Alpha Index |
| ```-i``` | View task information. | Target Alpha Index |
| ```-a``` | Switch to archive view. | None |
| ```-m``` | Switch to main/default view. | None |
| ```-t``` | Switch tabs. | Tab Name |
| ```-s``` | Save task database. | None |
| ```-p``` | Clean up ("prune") old database savestates. | None |
| ```-k``` | Close ("kill") application. | None |

[^1]: See [Theory of Operation](url). 
[^2]: Behavior of delete command is context specific. See [Delete a Task](url).










