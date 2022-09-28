import click


class RunGroup(click.Group):
    default_command: str

    def command(self, *args, **kwargs):
        default_command = kwargs.pop("default_command", False)
        if default_command and not args:
            kwargs["name"] = kwargs.get("name", "<>")
        decorator = super(RunGroup, self).command(*args, **kwargs)

        if default_command:

            def new_decorator(f):
                cmd = decorator(f)
                self.default_command = cmd.name or "default"
                return cmd

            return new_decorator

        return decorator

    def resolve_command(self, ctx, args):
        try:
            return super(RunGroup, self).resolve_command(ctx, args)
        except click.UsageError:
            args.insert(0, self.default_command)
            return super(RunGroup, self).resolve_command(ctx, args)
