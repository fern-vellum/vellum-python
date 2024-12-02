# Workflow Codegen

This is used to generate the code representation of a Vellum Workflow given its JSON display representation.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Updating this README](#updating-this-readme)
- [Setup](#setup)
- [Testing](#testing)
  - [Tips for Writing Tests](#tips-for-writing-tests)
    - [Unit Testing](#unit-testing)
    - [Integration Testing](#integration-testing)
- [Developing Alongside Fern](#developing-alongside-fern)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Updating this README

This README is generated using [doctoc](https://github.com/thlorenz/doctoc)

To install doctoc, run `npm install -g doctoc`

To update the table of contents, run `doctoc README.md`

## Setup

1. Install `nvm` to manage Node versions by following the instructions [here](https://github.com/nvm-sh/nvm) or
   check your `nvm` version with `nvm ---version`.
2. Install the version of Node we rely on by running:
   ```bash
   nvm install v18.12.1
   ```
3. Ensure you're using Node 18 by default via:
   ```bash
   nvm alias default v18.12.1
   ```
4. Use `npm` to install the project dependencies:
   ```bash
   npm install
   ```
5. If you haven't already, go to the CONTRIBUTING.md guide and run the setup steps there

## Testing

To run unit tests:

For these tests to run successfully, you'll need to run the poetry virtual environment.
The steps to set this up are in the README at the root of this repo.

```bash
npm run test
```

Many tests rely on snapshots. If you've changed logic such that the snapshot is intentionally different, you
can update snapshots by running:

```bash
npm run test:update
```

To validate types:

```bash
npm run types
```

### Tips for Writing Tests

There are two types of tests in this package.

#### Unit Tests

Unit tests test individual generators in isolation. For example, you might write a unit test to validate that
`TextSearchNode` generates the correct python code given its JSON representation.

Unit tests should use snapshot testing to validate the generated code. For example,

```typescript
it("TextSearchNode", async () => {
  const node = new TextSearchNode({
    workflowContext,
    nodeData,
  });

  node.getNodeFile().write(writer);
  expect(await writer.toStringFormatted()).toMatchSnapshot();
});
```

#### Integration Tests

Integration tests test the entire code generation process for a complete Workflow. The way they work is we automatically
traverse the `workflows/codegen/tests/fixtures` directory and run the tests on each `.json` file in that directory.

`codegen/src/__test__/project.test.ts` is responsible for running these integration tests.

## Developing Alongside Fern

We use fern's python [codegen package](https://github.com/fern-api/fern/tree/main/generators/python-v2/codegen) to
generate the python code representation of a Vellum Workflow. In some cases, you might find that fern doesn't yet have
support for constructing the python syntax you need. In these cases, we can contribute to fern's open source repo directly.

It's usually best to implement your changes in fern locally and confirm that they fulfill your needs in this repo
before opening the PR to fern with your changes. To make changes to fern's python codegen package and test those
changes in the workflow codegen package locally, follow these steps:

1. Clone the fern repository
   ```bash
   git clone git@github.com:fern-api/fern.git
   ```
2. Update the `"@fern-api/python-ast"` dependency in `package.json` to point to the local fern repository.
   It should be the relative file path to the `ast` directory in this repository.
   ```json
   "@fern-api/python-ast": "file:../../../fern-api/fern/generators/python-v2/ast/lib",
   ```
3. Run `npm install` to install the updated dependency.
4. Navigate to the `fern` repo and be sure to pull the `vargas/publish-python-ast` branch.
5. Make changes to the fern python ast package.
6. After making changes, run `pnpm dist` within `fern/generators/python-v2/ast` to compile the changes.
7. Navigate back to this repo and make use of these changes
8. Open a PR of the commit in its own branch (separate from the `vargas/publish-python-ast` branch) in the fern repository to merge your changes.
9. Work with a Vellum Admin to cut a new release of the package as we'll need to rebase the `vargas/publish-python-ast`
   branch
10. Update the dependency in this repo to the new version.

## Publishing

This package is meant to be versioned along with the Vellum Python SDK. When incrementing to match the latest Vellum Python SDK version, run:

```bash
npm version patch|minor|major
```

However, there are times where we need to publish a new version of this package without incrementing the Vellum Python SDK version. In this case, we increment the version using the prerelease strategy:

```bash
npm run version:codegen
```

This will bump the version from `0.2.6` to `0.2.6-post1`, `0.2.6-post2`, etc. It's important to note that **this is not SemVer Compliant**. SemVer doesn't have a concept of doing postreleases well, and technically speaking, does not consider `0.2.6-post1` to be later than `0.2.6`. Given that this package is only used internally for now, this is not a huge deal, but it's something to be aware of. If we wanted to be SemVer compliant, then we would have to choose a different versioning strategy. The alternatives are not ideal, but they are:

- Version codegen and the sdk independently.
- Version the SDK with just majors and minors going forward, opening up patch versions for codegen.

We have a GitHub Action that will publish all of the patch versions to NPM (i.e, the ones without a `-post` suffix). If that action fails, or we need to publish a post-release version, we'll need to publish manually.

To publish a package manually, you'll need to run the following commands locally:

```bash
npm run gar-login
npm publish
```

_Note: For some reason, the `gar-login` command doesn't work as part of the `prepublish` script, so it needs to be run separately._
