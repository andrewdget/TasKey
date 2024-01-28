# Change Log

## alpha2 (Feb, xx, 2024)

<ul>
	<li><b>Complete overhaul of user interface - cleaner, easier to read, maximizes screen space, and vast improvement to availability of "at a glance" information.</b></li>
	<br><li>New Features:
		<ul>
			<li>Implemented feature which allows tasks to be "hard" deleted 
			(accessible from the Archive view).</li>
			<li>Implemented arrow-key scrolling.</li>
			<li>Implemented manual database save function.</li>
		</ul>
	</li>
	<br><li>Bug Fixes:
		<ul>
			<li>Resolved issue that prevented the number of working days remaining to
				complete a task from updating correctly (also preventing priority score and list order from updating).</li>
			<li>Implemented better command input validation and error message handling, preventing application breaking additions to task database.</li>
			<li>Resolved issue where the use of hyphens in task name or footnote would incorrectly be interpreted as a flag. Hyphens are now tolerated, but only if bounded by two words without a space i.e. "high-profile".</li>
			<li>Date display format now consistent with date input format.</li>
			<li>Resolved issue that prevented the updating of save location once a database was created.</li>
		</ul>
	</li>
	<br><li>Mics. Housekeeping:
		<ul>
			<li>Renamed "src" directory to "TasKey" for readability as there is no current intent to add TasKey to package index.</li>
			<li>Moved common functions from DataStructure.py and CommandProcessor.py to Utils.py for simplicity.</li>
			<li>Cleaned up long (over 80 char) inline comments, corrected spelling errors, reordered/grouped related functions, etc.</li>
		</ul>
	</li>
</ul>


## alpha (Dec 19, 2023)

Functioning version of TasKey entering alpha testing/development.

## proto (Dec 19, 2023)

Earliest "functioning" version of TasKey.
