package dk.itu_real.open_evolution.MinecraftExtendedCommands.command;



/*
 * This file is part of SimpleMail, licensed under the MIT License (MIT).
 *
 * Copyright (c) 2015 Felix Schmidt <https://github.com/boformer>
 * Copyright (c) contributors
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

import org.slf4j.Logger;
import org.spongepowered.api.block.BlockType;
import org.spongepowered.api.command.CommandException;
import org.spongepowered.api.command.CommandResult;
import org.spongepowered.api.command.CommandSource;
import org.spongepowered.api.command.args.CommandContext;
import org.spongepowered.api.command.spec.CommandExecutor;
import org.spongepowered.api.text.Text;
// import org.spongepowered.api.text.Text;
import org.spongepowered.api.world.Location;
import org.spongepowered.api.world.World;

import com.google.gson.Gson;
// import org.spongepowered.api.world.WorldArchetypes;

/**
 * The Command to get block type on coordinate.
 */
public class BulkBlockSet implements CommandExecutor {

    // private MinecraftExtendedCommands plugin;
    private Logger logger;

    public BulkBlockSet(Logger logger) {
        this.logger = logger;
    }

    @Override
    public CommandResult execute(CommandSource src, CommandContext args) throws CommandException {
        @SuppressWarnings("unchecked")
        String json_package = (String) args.getOne("json_package").orElse(null);
        Gson gson = new Gson();
        String[] listOfStrings = gson.fromJson(json_package, String[].class);
        
        for(String blockDataJSON: listOfStrings) {
        	String[] blockData = gson.fromJson(blockDataJSON, String[].class);
        	String b_type = blockData[0];
        	int x_coord = Integer.parseInt(blockData[1]);
        	int y_coord = Integer.parseInt(blockData[2]);
        	int z_coord = Integer.parseInt(blockData[3]);
        	
        	String msg = "Block type: " + b_type + "-> " + x_coord + ", " + y_coord + ", " + z_coord;
        	System.out.println(msg);
        	logger.info(msg);
        	src.sendMessage(Text.of(msg));
        }
        return CommandResult.success();
    }
}