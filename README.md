## black-primer

> NOTICE: **This repository exists as a historical record, active development is not
> planned.**
>
> `black-primer` is an obsolete tool (now replaced with [diff-shades]) that was used to
> gauge the impact of changes in _Black_ on open-source code. It is no longer used
> internally and was moved into its own repository in March 2022.

`black-primer` is a tool built for CI (and humans) to have _Black_ `--check` a number of
Git accessible projects in parallel. (configured in `primer.json`) _(A PR will be
accepted to add Mercurial support.)_

## Run flow

- Ensure we have a `black` + `git` in PATH
- Load projects from `primer.json`
- Run projects in parallel with `--worker` workers (defaults to CPU count / 2)
  - Checkout projects
  - Run black and record result
  - Clean up repository checkout _(can optionally be disabled via `--keep`)_
- Display results summary to screen
- Default to cleaning up `--work-dir` (which defaults to tempfile schemantics)
- Return
  - 0 for successful run
  - \< 0 for environment / internal error
  - \> 0 for each project with an error

## Speed up runs 🏎

If you're running locally yourself to test black on lots of code try:

- Using `-k` / `--keep` + `-w` / `--work-dir` so you don't have to re-checkout the repo
  each run

## CLI arguments

```
Usage: black-primer [OPTIONS]

  primer - prime projects for blackening... 🏴

Options:
  -c, --config PATH      JSON config file path  [default:
                         /home/ichard26/programming/oss/black-
                         primer/src/black_primer/primer.json]

  --debug                Turn on debug logging  [default: False]
  -k, --keep             Keep workdir + repos post run  [default: False]
  -L, --long-checkouts   Pull big projects to test  [default: False]
  --no-diff              Disable showing source file changes in black output
                         [default: False]

  --projects TEXT        Comma separated list of projects to run  [default: ST
                         DIN,aioexabgp,attrs,bandersnatch,channels,cpython,dja
                         ngo,flake8-bugbear,hypothesis,pandas,pillow,poetry,pt
                         r,pyanalyze,pyramid,pytest,scikit-
                         lego,tox,typeshed,virtualenv,warehouse]

  -R, --rebase           Rebase project if already checked out  [default:
                         False]

  -w, --workdir PATH     Directory path for repo checkouts  [default:
                         /tmp/primer.20220314212941]

  -W, --workers INTEGER  Number of parallel worker coroutines  [default: 2]
  -h, --help             Show this message and exit.
```

[diff-shades]: https://github.com/ichard26/diff-shades
