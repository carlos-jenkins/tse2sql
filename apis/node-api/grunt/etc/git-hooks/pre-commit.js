var exec = require('child_process').exec,
    sh = require('execSync').run;

// http://viget.com/extend/grunt-getting-started-with-git-hooks
exec('git diff --cached --quiet', function (err, stdout, stderr) {
  // only run if there are staged changes
  // i.e. what you would be committing if you ran "git commit" without "-a" option.
  if (err) {

    // stash unstaged changes - only test what's being committed
    sh('git stash --keep-index --quiet');

    exec('grunt {{task}}', function (err, stdout, stderr) {

      console.log(stdout);

      // restore stashed changes
      sh('git stash pop --quiet');

      var exitCode = 0;
      if (err) {
        console.log(stderr);
        exitCode = -1;
      }
      process.exit(exitCode);
    });
  }
});
